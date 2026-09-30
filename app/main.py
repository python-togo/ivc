from fastapi import FastAPI
from app.core.gdrive import generate_certificate
from app.core.settings import config
from app.schema.models import Certificate, CertificateResponse


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Certificate Generator API. Visit /docs for API documentation."}


@app.post("/generate-certificate", response_model=CertificateResponse)
async def generate_certificate_endpoint(certificate: Certificate):
    response = generate_certificate(
        certificate.full_name, config.gslides_template_id)
    return response[0]  # Return only the response dictionary, not the stream
