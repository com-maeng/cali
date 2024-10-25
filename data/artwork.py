import os
import io
import logging

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from dtos import Artwork


class ArtworkDataPipeline:
    def __init__(self) -> None:
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        self.service_account_file = 'service_account_key.json'
        self.creds = Credentials.from_service_account_file(
            self.service_account_file)

        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

        self.sheet = self.sheets_service.spreadsheets()  # pylint: disable=no-member
        self.artworks = []

    def __get_new_artworks(self) -> bool:
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

        if not self.artworks:
            return False  # No artworks to update

        return True

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

                artwork.image_streams.append(image_stream)

    def activate_pipeline(self) -> bool:
        if not self.__get_new_artworks():
            logging.info('새로 적재할 artwork가 없습니다.')
            return True

        self.__get_artwork_files()

        # TODO
        # self.__load_artwork_files_to_bucket()
        # self.__split_artworks_into_hanja()
        # self.__label_hanja()
        # self.__load_hanja()
