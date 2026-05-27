"""
Google Workspace OAuth helper.
Authenticates once, saves token for reuse.
Supports: Gmail, Calendar, Drive.
"""
import os
import json
import sys
import ssl
import urllib3
from pathlib import Path

import requests as _requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

_http_session = _requests.Session()
_http_session.verify = False

TOKEN_PATH = Path(__file__).parent / "token.json"
CREDS_PATH = Path(__file__).parent / "credentials.json"

# All scopes we need
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/contacts.readonly",
]


def get_credentials() -> Credentials:
    """Return valid credentials, refreshing or re-authenticating as needed."""
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request(session=_http_session))
        else:
            if not CREDS_PATH.exists():
                print(
                    "ERROR: credentials.json not found.\n"
                    "Go to https://console.cloud.google.com/apis/credentials\n"
                    "Create an OAuth 2.0 Client ID (Desktop app) and download the JSON.\n"
                    f"Save it as: {CREDS_PATH}",
                    file=sys.stderr,
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_PATH.write_text(creds.to_json())

    return creds


def build_service(service_name: str, version: str):
    """Build a Google API service client with SSL verification disabled (Windows fix)."""
    import httplib2
    from googleapiclient.discovery import build as gapi_build
    from google_auth_httplib2 import AuthorizedHttp

    creds = get_credentials()
    http = httplib2.Http(disable_ssl_certificate_validation=True)
    authed_http = AuthorizedHttp(creds, http=http)
    return gapi_build(service_name, version, http=authed_http)


if __name__ == "__main__":
    creds = get_credentials()
    print(f"Authenticated. Token saved to {TOKEN_PATH}")
