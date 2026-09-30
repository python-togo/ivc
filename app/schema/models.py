from pydantic import BaseModel, Field


class Config(BaseModel):
    """
    Configuration model for the application.
    """
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    verification_base_url: str = Field(..., env="VERIFICATION_BASE_URL")
    gslides_template_id: str = Field(..., env="GSLIDES_TEMPLATE_ID")
    imagekit_public_key: str = Field(..., env="IMAGEKIT_PUBLIC_KEY")
    imagekit_private_key: str = Field(..., env="IMAGEKIT_PRIVATE_KEY")
    imagekit_url_endpoint: str = Field(..., env="IMAGEKIT_URL_ENDPOINT")
    credentials_path: str = Field(..., env="CREDENTIALS_PATH")
    token_path: str = Field(..., env="TOKEN_PATH")
    sender_email: str = Field(..., env="SENDER_EMAIL_ADDRESS")
    sender_name: str = Field(..., env="SENDER_NAME")
    # Sheet containing names and email address.
    gsheets_id: str = Field(..., env="GSHEETS_ID")
    # SMTP configuration
    smtp_user: str = Field(..., env="STMP_USER")
    smtp_password: str = Field(..., env="STMP_PASSWORD")
    smtp_server: str = Field(..., env="STMP_HOST")
    smtp_port: int = Field(..., env="STMP_PORT")
    backend_url: str = Field(..., env="BACKEND_URL")
    event_code: str = Field(..., env="EVENT_CODE")
    api_key: str = Field(..., env="API_KEY")


class Certificate(BaseModel):
    """
    Model representing a certificate.
    """
    full_name: str


class CertificateResponse(BaseModel):
    """
    Model representing the response after generating a certificate.
    """
    full_name: str
    verifiable_url: str
    code: str
    pdf_url: str
