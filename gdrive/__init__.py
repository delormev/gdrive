import httplib2
import urllib
import json
from oauth2client.service_account import ServiceAccountCredentials

class GoogleDriveCon:
	# Defines scope and base URL
	scope = ['https://www.googleapis.com/auth/drive.metadata','https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
	baseUrl = 'https://www.googleapis.com/drive/v3/files/'

	# Creates connection based on access file
	def __init__(self, access_file):
		self.access_file = access_file

	def _queryDrive(self, method, query):
		credentials = ServiceAccountCredentials.from_json_keyfile_name(self.access_file, self.scope)
		http = credentials.authorize(httplib2.Http())
		resp, content = http.request(
		    uri=self.baseUrl + query,
		    method=method,
		)
		return resp, content

	# Public functions

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
				return ""
			else:
				exportMime = None
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return ""

		if (exportMime):
			resp, content = self._queryDrive('GET', fileId + '/export' + '?' + urllib.urlencode( { "mimeType": exportMime } ))
		else:
			resp, content = self._queryDrive('GET', fileId +  '?' + urllib.urlencode( { "alt": "media" } ))

		if (resp['status'] == '200'):
			return content
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return ""
	
	# Lists files in the specified folder
	# TODO: add a way to specify format of the export
	def listFiles(self, folderId):
		resp, content = self._queryDrive('GET', folderId)
		
		if (resp['status'] == '200'):
			files_json = json.loads(content)
			if not (files_json['mimeType'].endswith('folder')):
				print '[ERROR] Google ID specified is not a folder.'
				return []

		resp, content = self._queryDrive('GET', '?' + urllib.urlencode( { "q": "'0BxEvfXu_ejXDRGlSVTh6ZDJuR0k' in parents", "orderBy": "modifiedTime"} )) 

		if (resp['status'] == '200'):
			files_json = json.loads(content)
			return files_json["files"]
		else:
			print '[ERROR] ' + str(resp) + '\n' + str(content)
			return []