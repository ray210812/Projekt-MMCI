import json

from googleapiclient.http import MediaFileUpload
import sql
import os.path
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle


SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate_google_drive():
  creds = None
  # Überprüfen, ob bereits ein gültiges Token existiert
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)


  service = build('drive', 'v3', credentials=creds)
  return service


def update_file():
  sql.getInformationasJSON()
  service = authenticate_google_drive()
  media = MediaFileUpload('./test.json', mimetype='application/json')
  updated_file = service.files().update(fileId='1xlSnRHHgoCA6qoC_eCOUvqGk-gpA58vu', media_body=media).execute()
  print('Updated File ID:', updated_file['id'])


update_file()
