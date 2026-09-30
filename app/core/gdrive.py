
from httpx import stream

from app.core.gmail import send_email, send_email_pro
from app.core.google_api import gdrive_service, gslides_service
from datetime import datetime
from uuid import uuid4
from app.utils.imagekit import upload_file_base64_url, upload_pdf_file_stream
from app.core.settings import config
import httpx
import asyncio


def copy_presentation(source_presentation_id, filename):
    body = {"name": filename}
    drive_response = (
        gdrive_service.files().copy(fileId=source_presentation_id, body=body).execute()
    )
    # the id of the newly created presentation
    presentation_copy_id = drive_response.get("id")
    return presentation_copy_id


def get_qr_code_object_id(presentation_id, title_tag="QR_CODE_PLACEHOLDER"):
    """
    Parcourt les diapositives pour récupérer l'objectId de l'image QR code
    à partir de son Texte de Remplacement (Alt Text / Title).
    """
    presentation = gslides_service.presentations().get(
        presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])

    first_slide = slides[0] if slides else []
    page_elements = first_slide.get('pageElements', []) if first_slide else []

    for element in page_elements:
        element_title = element.get('title', '')
        element_desc = element.get('description', '')

        if element_title == title_tag or element_desc == title_tag:
            return element.get('objectId')

    return None


def update_slide_content(presentation_id, attendee_name, filename=None):
    # Create the requests to update the slide content
    response = {}
    new_id = str(uuid4())[:8].upper()
    qr_object_id = get_qr_code_object_id(
        presentation_id, title_tag="QR_CODE_PLACEHOLDER")

    print(attendee_name)

    date_string = datetime.now().strftime("%b %d, %Y")
    requests = [
        {
            "replaceAllText": {
                "containsText": {
                    "text": "{{blog-reader-name}}",
                    "matchCase": True,
                },
                "replaceText": attendee_name,
            }
        },
        {
            "replaceAllText": {
                "containsText": {
                    "text": "{{issue-date}}",
                    "matchCase": True,
                },
                "replaceText": f"{date_string}",
            }
        }
    ]

    verifiable_url = f"{config.verification_base_url}/{new_id}"

    if qr_object_id:
        new_qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={verifiable_url}"
        requests.append({
            'replaceImage': {
                'imageObjectId': qr_object_id,
                'url': new_qr_code_url,
                # 'INSIDE' adapte la nouvelle image au cadre de l'ancienne sans la déformer ni la rogner
                'imageReplaceMethod': 'CENTER_INSIDE'
            }
        })

    body = {"requests": requests}
    gslides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body=body).execute()

    stream = gdrive_service.files().export(fileId=presentation_id,
                                           mimeType="application/pdf").execute()

    if not filename:
        filename = f"{attendee_name.translate(str.maketrans(' ', '_'))}_pycontg26_certificat.pdf"

    result = upload_pdf_file_stream(
        filename=filename,
        stream=stream,
        folder="pycontogo26"
    )

    response = {
        "full_name": attendee_name,
        "verifiable_url": verifiable_url,
        "description": f"Certificate for {attendee_name} generated on {date_string}",
        "code": new_id,
        "pdf_url": result.url,
        "is_revoked": False
    }

    return response, stream


def normalize_name(name):
    """"""
    full_name = ""
    for name_part in name.split():
        if len(name_part) > 2:
            full_name += name_part.capitalize() + " "
        else:
            full_name += name_part.upper() + " "

    return full_name.strip()


async def generate_certificate(attendee_name, slide_template_id, type="volunteer"):
    unique_id = str(uuid4())[:8]
    attendee_name = normalize_name(attendee_name)
    filename = f"{attendee_name.translate(str.maketrans(' ', '_'))}_{unique_id}_certificat"
    new_slide_id = copy_presentation(slide_template_id, filename)
    response, stream = update_slide_content(
        new_slide_id, attendee_name, filename=filename)

    async with httpx.AsyncClient() as client:
        await client.post(
            f"{config.backend_url}/certificates/generate/{config.event_code}?type={type}",
            json=response,
            headers={"Authorization": f"Bearer {config.api_key}"}
        )
    return response, stream, filename


if __name__ == "__main__":
    from app.core.gsheet import values
    from app.utils.email_template import volunteer_email_plain, volunteer_email_html, email_subject, email_staff_html, email_staff_plain
    # Example usage
    for row in values:

        attendee_name = row[1]
        attendee_email = row[2]
        first_name = attendee_name.split()[-1].capitalize()

        response, stream, filename = asyncio.run(
            generate_certificate(attendee_name, config.gslides_template_id, type="staff"))

        print(f"Generated certificate for {attendee_name} ({attendee_email})")

        subject = email_subject
        sender_name = "PyCon Togo 2026 team"
        sender_email = "team@pytogo.org"
        body_plain = email_staff_plain.replace(
            "{first_name}", first_name)
        body_html = email_staff_html.replace("{first_name}", first_name)
        recipients = [attendee_email]

        send_email_pro(subject, sender_name=sender_name, sender_email=sender_email, body_plain=body_plain,
                       body_html=body_html, recipients=recipients, filename=filename, attachment=stream)
