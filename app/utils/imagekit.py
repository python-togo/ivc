import base64

from imagekitio import ImageKit
from app.core.settings import config

_client: ImageKit | None = None


def _get_client() -> ImageKit:
    global _client
    if _client is None:
        if not config.imagekit_private_key:
            raise RuntimeError(
                "IMAGEKIT_PRIVATE_KEY is not set. Configure it to use ImageKit."
            )
        _client = ImageKit(private_key=config.imagekit_private_key)
    return _client


def upload_file_base64_url(filename: str, base64_string: str, folder: str = ""):
    try:
        client = _get_client()
        upload_response = client.files.upload(
            file=base64.b64decode(base64_string),
            file_name=filename,
            folder="/certificates/" + folder.lstrip("/"),
        )
        return upload_response
    except Exception as e:
        raise Exception(f"Error uploading image: {str(e)}")


def upload_pdf_file_stream(filename: str, stream: bytes, folder: str = ""):
    try:
        client = _get_client()
        upload_response = client.files.upload(
            file=stream,
            file_name=filename,
            folder="/certificates/" + folder.lstrip("/"),
        )

        # upload_response.url will contain the URL of the uploaded PDF file
        return upload_response
    except Exception as e:
        raise Exception(f"Error uploading PDF: {str(e)}")
