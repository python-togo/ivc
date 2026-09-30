from decouple import config
from app.schema.models import Config


config = Config(
    google_api_key=config("GOOGLE_API_KEY"),
    verification_base_url=config("VERIFICATION_BASE_URL").rstrip('/'),
    gslides_template_id=config("GSLIDES_TEMPLATE_ID"),
    imagekit_public_key=config("IMAGEKIT_PUBLIC_KEY"),
    imagekit_private_key=config("IMAGEKIT_PRIVATE_KEY"),
    imagekit_url_endpoint=config("IMAGEKIT_URL_ENDPOINT"),
    credentials_path=config("CREDENTIALS_PATH"),
    token_path=config("TOKEN_PATH"),
    sender_email=config("SENDER_EMAIL_ADDRESS"),
    sender_name=config("SENDER_NAME"),
    gsheets_id=config("GSHEETS_ID"),
    smtp_user=config("STMP_USER"),
    smtp_password=config("STMP_PASSWORD"),
    smtp_server=config("STMP_HOST"),
    smtp_port=config("STMP_PORT", cast=int),
    backend_url=config("BACKEND_URL").rstrip('/'),
    event_code=config("EVENT_CODE"),
    api_key=config("API_KEY")
)
