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
# url = 'https://media.licdn.com/dms/document/media/D4D1FAQERVMQwpJkmhg/feedshare-document-pdf-analyzed/0/1697112639826?e=1698278400&v=beta&t=D1GVhm8vHajuOexSvqQlQADk2a8wYprCOqaomFaNNCM'
# NAME = 'RemoteWork'

def get_content(url):
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        print('Getting pdf from link',response.status_code)
        pdf_content = response.content
        return pdf_content
    else:
        print(response)
        print("Failed to download file: {}".format(response.status_code))
def authenticate():
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    return creds

def upload_pdf(url,name,folder_id):
    extention = get_file_extension(url)
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    if extention == 'gif':
        id = "1_nP_0ZQzhJMu_yng33KZdEyYmAjiXBGa"
        file_metadata = {
            'name' : name,
            'parents' : [id]
        } 
        content = get_content(url)
        media = MediaIoBaseUpload(BytesIO(content), mimetype='image/gif')
        return f"{name}.gif file upladed to gif folder"
    elif extention == 'pdf':
        file_metadata = {
            'name' : name,
            'parents' : [folder_id]
        }
        pdf_content = get_content(url)
        media = MediaIoBaseUpload(BytesIO(pdf_content), mimetype='application/pdf')
        return f"{name}.pdg file upladed to PDF folder"
    else:
        pass

    file = service.files().create(
        body=file_metadata,
        media_body=media
    ).execute()


def get_file_extension(url):
    try:
        response = requests.head(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

        # Check if the server provided a Content-Type header
        content_type = response.headers.get('Content-Type')
        if content_type:
            # Extract the file extension from the Content-Type header
            _, extension = content_type.split('/')
            return extension
        else:
            print("Error: Content-Type header not found in the response.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# upload_pdf(url,NAME,PARENT_FOLDER_ID)