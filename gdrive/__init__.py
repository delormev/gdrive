import httplib2
import urllib
import json
from oauth2client.service_account import ServiceAccountCredentials
import sys

class GoogleDriveCon:
	# Defines scope and base URL
	scope = ['https://www.googleapis.com/auth/drive.metadata','https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
	baseUrl = 'https://www.googleapis.com/drive/v3/files/'

	# Creates connection based on access file
	def __init__(self, access_file):
		self.access_file = access_file

	def _queryDrive(self, method, query, body=None):
		print json.dumps(body) if body else "None"
		credentials = ServiceAccountCredentials.from_json_keyfile_name(self.access_file, self.scope)
		http = credentials.authorize(httplib2.Http())
		resp, content = http.request(
		    uri=self.baseUrl + query,
		    method=method,
		    body=body,
		)
		return resp, content

	# Public functions

	# Change owner for the specificed file to email address
	def changeOwner(self, objectId, email):
		resp, content = self._queryDrive('GET', objectId)
		
		if (resp['status'] == '200'):
			params = { "role": "owner", "type": "user", "emailAddress": email }
		else:
			print '[ERROR] Google ID "' + objectId + '" does not exist.'
			return None

		resp, content = self._queryDrive('POST', objectId + '/permissions?' + urllib.urlencode({ "transferOwnership": True }), body=params)

		if (resp['status'] == '200'):
			files_json = json.loads(content)
			return files_json
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return None


	# Opens specific file. Defaults to CSV for spreadsheets, plain text for everything else
	# TODO: add a way to specify format of the export
	def openFile(self, fileId):
		resp, content = self._queryDrive('GET', fileId)
		
		if (resp['status'] == '200'):
			files_json = json.loads(content)
			if files_json['mimeType'].endswith('spreadsheet'):
				exportMime = "text/csv"
			elif files_json['mimeType'].endswith('spreadsheet'):
				exportMime = "text/plain"
			elif files_json['mimeType'].endswith('folder'):
				print '[ERROR] Cannot stream a folder.'
				return None
			else:
				exportMime = None
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return None

		if (exportMime):
			resp, content = self._queryDrive('GET', fileId + '/export' + '?' + urllib.urlencode( { "mimeType": exportMime } ))
		else:
			resp, content = self._queryDrive('GET', fileId +  '?' + urllib.urlencode( { "alt": "media" } ))

		if (resp['status'] == '200'):
			return content
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return None
	
	# Lists files in the specified folder
	# Returns list of file objects, like so: { "kind": "drive#file", "id": string, "name": string, "mimeType": string }
	def listFiles(self, folderId):
		resp, content = self._queryDrive('GET', folderId)
		
		if (resp['status'] == '200'):
			files_json = json.loads(content)
			if not (files_json['mimeType'].endswith('folder')):
				print '[ERROR] Google ID specified is not a folder.'
				return []

		resp, content = self._queryDrive('GET', '?' + urllib.urlencode( { "q": "'" + folderId + "' in parents", "orderBy": "modifiedTime"} )) 

		if (resp['status'] == '200'):
			files_json = json.loads(content)
			return files_json["files"]
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return []

	# Create folder in the specified folder
	# Retuns a file object, like so: { "kind": "drive#file", "id": string, "name": string, "mimeType": string }
	def makeFolder(self, folderId, folderName, owner):
		files = self.listFiles(folderId)
		
		if (len(filter(lambda x: (x["mimeType"].endswith("folder") and (x["name"] == folderName)), files)) > 0):
			print '[ERROR] Folder "' + folderName + '" already exists in folder with Google ID ' + folderId
			return None

		file_metadata = {
			"name" : folderName,
			"mimeType" : "application/vnd.google-apps.folder",
			"parents": [ folderId ]
		}

		resp, content = self._queryDrive('POST', '', body=file_metadata) 

		if (resp['status'] == '200'):
			files_json = json.loads(content)
			print files_json
			return None
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return None

		return changeOwner(self, objectId, email)

	# Move file into the specified folder
	# Retuns a file object, like so: { "kind": "drive#file", "id": string, "name": string, "mimeType": string }
	def moveObject(self, objectId, newParentFolderId):
		resp, content = self._queryDrive('GET', objectId + '?' + urllib.urlencode({ "fields": "parents" }))
		
		if (resp['status'] == '200'):
			file_json = json.loads(content)
			oldParents = ",".join(file_json['parents'])
		else:
			print '[ERROR] Google ID "' + objectId + '" does not exist.'
			return None

		resp, content = self._queryDrive('PATCH', objectId + '?' + urllib.urlencode({ "addParents": newParentFolderId, "removeParents": oldParents })) 

		if (resp['status'] == '200'):
			files_json = json.loads(content)
			return files_json["files"]
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return None

