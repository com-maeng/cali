import io

from PIL import Image


def convert_stream_to_webp(file_stream: io.BytesIO) -> io.BytesIO:
    image = Image.open(file_stream)
    output_file_stream = io.BytesIO()

    image.save(output_file_stream, format='WEBP')

    return output_file_stream
