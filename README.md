# gdrive

Python wrapper for the Google Drive API

## Installation

> pip install https://github.com/delormev/google-drive/zipball/master

## Usage

```python
import gdrive

conn = gdrive.GoogleDriveCon('/path/to/.google_access_keys.json')
test = conn.openFile('MyGDriveFileId')
```