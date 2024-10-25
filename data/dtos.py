import io

from dataclasses import dataclass


@dataclass
class Artwork:
    row_num: int
    artist_name: str
    artwork_name: str
    drive_url: str
    image_streams: list[io.BytesIO]
