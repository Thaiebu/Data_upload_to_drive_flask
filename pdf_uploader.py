from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO
import requests,json

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_DATA = 'service_account.json'
# print(SERVICE_ACCOUNT_DATA)
# PARENT_FOLDER_ID = "1CiQLVoG-fUML0d6KNHNuDxccuLuYBRBo"
# PDF_URL = 'https://media.licdn.com/dms/document/media/D4D1FAQERVMQwpJkmhg/feedshare-document-pdf-analyzed/0/1697112639826?e=1698278400&v=beta&t=D1GVhm8vHajuOexSvqQlQADk2a8wYprCOqaomFaNNCM'
# NAME = 'RemoteWork'

def get_pdf_content(pdf_url):
    pdf_response = requests.get(pdf_url)
    if pdf_response.status_code == 200:
        print('Getting pdf from link',pdf_response.status_code)
        pdf_content = pdf_response.content
        return pdf_content
    else:
        print(pdf_response)
        print("Failed to download file: {}".format(pdf_response.status_code))
def authenticate():
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    return creds

def upload_pdf(pdf_url,name,folder_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name' : name,
        'parents' : [folder_id]
    }
    pdf_content = get_pdf_content(pdf_url)
    media = MediaIoBaseUpload(BytesIO(pdf_content), mimetype='application/pdf')

    file = service.files().create(
        body=file_metadata,
        media_body=media
    ).execute()


# upload_pdf(PDF_URL,NAME,PARENT_FOLDER_ID)