import io
from typing import NoReturn

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


class StorageClient:
    def __init__(self):
        self.creds = Credentials.from_service_account_file(
            'service_account_key.json')
        self.storage_service = build('storage', 'v1', credentials=self.creds)

    def insert_bytes_object_into_bucket(
        self,
        fd: io.BytesIO,
        mimitype: str,
        bucket: str,
        file_name: str
    ) -> NoReturn:
        """Bytes 오브젝트를 GCS 버킷에 적재합니다."""

        media = MediaIoBaseUpload(
            fd,
            mimetype=mimitype,
        )

        self.storage_service.objects().insert(  # pylint: disable=no-member
            bucket=bucket,
            media_body=media,
            body={
                'name': file_name
            }
        ).execute()
