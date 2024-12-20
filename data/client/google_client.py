import os
import io
from typing import NoReturn

from google.cloud import vision
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


class StorageClient:
    def __init__(self):
        self.service_account_file = '/'.join([
            os.getenv('SECRETS_DIR'),
            f'{os.getenv('SERVICE_ACCOUNT_KEY_NAME')}.json'
        ])
        self.creds = Credentials.from_service_account_file(
            self.service_account_file)
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


class VisionAPIClient:
    def __init__(self):
        self.service_account_file = '/'.join([
            os.getenv('SECRETS_DIR'),
            f'{os.getenv('SERVICE_ACCOUNT_KEY_NAME')}.json'
        ])
        self.creds = Credentials.from_service_account_file(
            self.service_account_file)
        self.image_annotator_client = vision.ImageAnnotatorClient(
            credentials=self.creds)

    def text_detection(self, image: vision.Image) -> str:
        boxes = ''
        response = self.image_annotator_client.text_detection(  # pylint: disable=no-member
            image=image)

        # Parse and return boxes
        for text in response.text_annotations:
            if len(text.description) > 1:  # Entire text
                continue

            # TODO: Is text.description value a chinese character?
            recognized_character = text.description
            x1 = text.bounding_poly.vertices[0].x
            y1 = text.bounding_poly.vertices[0].y
            x2 = text.bounding_poly.vertices[2].x
            y2 = text.bounding_poly.vertices[2].y
            dummy_page_num = '0'

            boxes += ', '.join([recognized_character, str(x1),
                               str(y1), str(x2), str(y2), dummy_page_num])
            boxes += '\n'

        return boxes
