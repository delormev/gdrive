# gdrive

Python wrapper for the Google Drive API

## Installation

Clone this repository and install with:

```bash
python setup.py install
```

Or install with pip:

```bash
pip install https://github.com/delormev/gdrive/zipball/master
```

## Usage

1. Create a new [service account](https://console.developers.google.com/apis/credentials) and a matching [service account key](https://console.developers.google.com/apis/credentials) in Google's Developer Console. Make a note of the email address for your service account, and download the JSON file associated with your key
2. Share the documents and folders you wish to access with the service account (by sharing it with the associated email address)
3. Connect to your Google Drive and access your documents:

```python
import gdrive

# Connect to the Google Drive account
conn = gdrive.GoogleDriveCon('/path/to/.google_access_keys.json')

# List files in a folder
folderList = conn.listFiles('MyGDriveFolderId')

# Load content of the first file
fileContent = conn.openFile(folderList[0]["id"])

```
