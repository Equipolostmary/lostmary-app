# drive_upload.py

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials
import io

def conectar_drive(credentials_info):
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)
    return service

def subir_archivo_a_drive(service, archivo, nombre_archivo, carpeta_id):
    file_metadata = {
        'name': nombre_archivo,
        'parents': [carpeta_id]
    }
    media = MediaIoBaseUpload(io.BytesIO(archivo.read()), mimetype=archivo.type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')
