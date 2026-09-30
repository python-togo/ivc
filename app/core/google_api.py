# import the necessary libraries
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.core.settings import config


# These are the different scopes we need for the different Google APIs


SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]
# Google Slide template ID.
GSLIDES_TEMPLATE_ID = config.gslides_template_id
GSHEETS_ID = ""  # Sheet containing names and email address.

# "credentials.json" is the credentials you get after you created the Google Cloud project

# Debugging line to check if credentials are loaded correctly


def authorize_google():
    credentials = None
    if os.path.exists(config.token_path):

        credentials = Credentials.from_authorized_user_file(
            config.token_path, SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(config.token_path, "w") as token:
            token.write(credentials.to_json())

    return credentials


credentials = authorize_google()


api_key = config.google_api_key  # Load the API key from environment variable

# Debugging line to check if the API key is loaded correctly

gdrive_service = build(
    "drive", "v3", credentials=credentials)
gslides_service = build(
    "slides", "v1", credentials=credentials)
gmail_service = build(
    "gmail", "v1", credentials=credentials)
gsheets_service = build(
    "sheets", "v4", credentials=credentials)
