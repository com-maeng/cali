import os
import io
import logging

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError

from data.dtos import Artwork
from data.utils.image_module import convert_stream_to_webp


class ArtworkDataPipeline:
    def __init__(self) -> None:
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        self.service_account_file = 'service_account_key.json'
        self.creds = Credentials.from_service_account_file(
            self.service_account_file)

        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.storage_service = build('storage', 'v1', credentials=self.creds)

        self.sheet = self.sheets_service.spreadsheets()  # pylint: disable=no-member
        self.artworks = []

    def __get_new_artworks(self):
        sheet_range = '시트1!B:H'
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                         range=sheet_range).execute()

        for idx, row in enumerate(result['values'][2:]):  # 0, 1번째 row는 패스
            if row[-1] == 'Y':
                continue  # 이미 적재된 작품

            if row[-1] != '정상':
                continue  # 검수 미완료 데이터

            artwork = Artwork(
                row_num=idx + 1,
                artist_name=row[0],
                artwork_name=row[1],
                drive_url=row[4],
                image_streams=[]  # Dummy
            )
            self.artworks.append(artwork)

            logging.info(
                '새로 적재할 artwork: %s - %s',
                artwork.artist_name,
                artwork.artwork_name
            )

    def __get_artwork_files(self) -> None:
        for artwork in self.artworks:
            folder_id = artwork.drive_url.replace(
                'https://drive.google.com/drive/folders/', '')
            folder_id = folder_id.replace('?usp=drive_link', '')
            q = f'\'{folder_id}\' in parents and trashed = false'

            files = self.drive_service.files().list(  # pylint: disable=no-member
                q=q,
                orderBy='name_natural'
            ).execute()['files']

            for file in files:
                request = self.drive_service.files().get_media(  # pylint: disable=no-member
                    fileId=file['id'])
                image_stream = io.BytesIO()
                downloader = MediaIoBaseDownload(image_stream, request)

                logging.info('Downloading %s ... 0%%', file['name'])

                while True:
                    # TODO: 다운로드 API 호출 예외처리 (timeout, etc.)
                    status, done = downloader.next_chunk()

                    logging.info('Downloading %s ... %d%%',
                                 file['name'], int(status.progress() * 100))

                    if done is True:
                        break

                artwork.image_streams.append({
                    'file_name': file['name'],
                    'image_stream': image_stream
                })

    def __load_artwork_streams_to_bucket(self, artwork: Artwork) -> ...:
        for stream in artwork.image_streams:
            file_name = stream['file_name']
            image_stream = stream['image_stream']

            converted_image_stream = convert_stream_to_webp(image_stream)
            uploader = MediaIoBaseUpload(
                converted_image_stream,
                mimetype='image/webp',
                resumable=True,
            )
            file_name_without_ext = file_name.rpartition('.')[0]
            file_name_with_path = '/'.join([
                artwork.artist_name,
                artwork.artwork_name,
                file_name_without_ext + '.webp',
            ])

            self.storage_service.objects().insert(  # pylint: disable=no-member
                bucket='cali-artwork-image',
                media_body=uploader,
                body={
                    'name': file_name_with_path
                }
            ).execute()  # TODO: 업로드 API 호출 예외처리 (timeout, etc.)

            logging.info('Uploaded %s', file_name_with_path)

    def __update_is_loaded_column(self, artwork: Artwork):
        range_name = f'시트1!H{artwork.row_num + 2}'  # 1, 2번째 컬럼이 포함된 행 번호
        body = {
            'values': [['Y']]
        }

        try:
            result = (
                self.sheet
                .values()
                .update(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name,
                    body=body,
                    valueInputOption='USER_ENTERED'
                )
                .execute()
            )
            logging.info(
                'Cell %s has been updated to \'Y\'',
                range_name
            )
        except HttpError as e:
            logging.error(e)

    def activate_pipeline(self) -> list[Artwork]:
        self.__get_new_artworks()

        if not self.artworks:
            return []

        self.__get_artwork_files()

        for artwork in self.artworks:
            # TODO: 작업이 실패했을 때에 대한 예외처리
            self.__load_artwork_streams_to_bucket(artwork)
            self.__update_is_loaded_column(artwork)

        return self.artworks
