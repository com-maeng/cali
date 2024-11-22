import io
import pytest

from data.client.google_client import StorageClient


@pytest.fixture(scope='module')  # 'data.tests.client.test_google_client'
def storage_client():
    return StorageClient()


def test_insert_bytes_object_into_bucket(mocker, storage_client):  # pylint: disable=redefined-outer-name
    fd = io.BytesIO(b'Dummy WEBP image data for test')
    mimetype = 'image/webp'
    bucket = 'dummy_bucket'
    file_name = 'dummy_image.webp'

    mock_objects = mocker.Mock()
    mock_storage_service = mocker.Mock()

    mock_storage_service.objects.return_value = mock_objects
    storage_client.storage_service = mock_storage_service

    storage_client.insert_bytes_object_into_bucket(
        fd, mimetype, bucket, file_name)

    mock_storage_service.objects.assert_called_once()
    mock_objects.insert.assert_called_once_with(
        bucket=bucket,
        media_body=mocker.ANY,
        body={'name': file_name}
    )
