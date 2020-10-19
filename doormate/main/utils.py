
from datetime import datetime, timedelta

import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def build_google_service(credentials):
    # creds = Credentials(token=token["access_token"], refresh_token=token["refresh_token"])
    service = build('calendar', 'v3', credentials=credentials)

    return service

def list_calendars(service):
    page_token = None
    calendars = []
    while True:
        response = service.calendarList().list(pageToken=page_token).execute()
        calendars += response["items"]
        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return calendars

def list_events(service, calendar="primary"):
    now = (datetime.utcnow() - timedelta(minutes=10)).isoformat() + 'Z'
    until = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

    events = service.events().list(calendarId=calendar, timeMin=now,
                                        timeMax=until, singleEvents=True,
                                        orderBy='startTime').execute()

    return events


def get_user_profile(token_type, access_token):
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo?alt=json",
        headers={"Authorization": f"{token_type} {access_token}"})

    response.raise_for_status()

    return response.json()
