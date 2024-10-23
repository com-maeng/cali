import os
import io
import logging

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from dtos import Artwork


class ArtworkDataPipeline:
    def __init__(self) -> None:
        self.service_account_file = 'service_account_key.json'
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')
        self.creds = Credentials.from_service_account_file(
            self.service_account_file)
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.sheets_service.spreadsheets()  # pylint: disable=no-member
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def __get_new_artworks(self) -> list[Artwork | None]:
        artworks = []
        sheet_range = '시트1!B:H'

        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                         range=sheet_range).execute()

        for row_idx, row in enumerate(result['values'][2:]):  # 0, 1번째 row는 패스
            if row[-1] == 'Y':
                continue  # 이미 적재된 작품

            if row[-1] != '정상':
                continue  # 검수 미완료 데이터

            artworks.append(
                Artwork(
                    row_num=row_idx + 1,  # 시트 내 행의 번호
                    artist_name=row[0],
                    artwork_name=row[1],
                    drive_url=row[4],
                    file_stream=io.BytesIO()  # Dummy instance
                )
            )

        return artworks

    def __get_files(self, artworks: list[Artwork]) -> None:
        for artwork in artworks:
            # Get file's ID from full URL
            file_id = artwork.drive_url.replace(
                'https://drive.google.com/file/d/', '')
            file_id = file_id.replace('/view?usp=drive_link', '')

            request = self.drive_service.files().get_media(  # pylint: disable=no-member
                fileId=file_id)
            downloader = MediaIoBaseDownload(artwork.file_stream, request)

            while True:
                _, done = downloader.next_chunk()  # TODO: 다운로드 API 호출 예외처리 (timeout, etc.)

                if done is True:
                    break

    def activate_pipeline(self) -> bool:
        artworks = self.__get_new_artworks()

        if not artworks:
            logging.info('새로 적재할 artwork가 없습니다.')
            return True

        self.__get_files(artworks)

        # TODO
        # self.__load_files()
        # self.__split_artwork_into_hanja()
        # self.__label_hanja()
        # self.__load_hanja()
