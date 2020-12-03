import json

from django.core.management.base import BaseCommand
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.helpers import session_from_client_secrets_file

from main.models import AuthInfo
from main.Scheduler import scheduler
from main.utils import build_google_service


class Command(BaseCommand):
    help = 'Initialises Scheduler with Event Fetcher Job'

    def handle(self, *args, **kwargs):
        auth_info = AuthInfo.objects.first()

        google_client_config = json.load(open('./doormate/credentials.json'))["web"]
        creds = Credentials(
            token=auth_info.access_token,
            refresh_token=auth_info.refresh_token,
            client_id=google_client_config["client_id"],
            client_secret=google_client_config["client_secret"],
            token_uri=google_client_config["token_uri"])

        google_service = build_google_service(creds)
        scheduler(google_service)
