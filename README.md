# gdrive

Python wrapper for the Google Drive API

## Installation

Clone this repository and install with:

```bash
python setup.py install
```

Or install with pip:

```bash
pip install https://github.com/delormev/google-drive/zipball/master
```

## Usage

```python
import gdrive

# Connect to the Google Drive account
conn = gdrive.GoogleDriveCon('/path/to/.google_access_keys.json')

# List files in a folder
folderList = conn.listFiles('MyGDriveFolderId')

# Load content of the first file
fileContent = conn.openFile(folderList[0]["id"])

```