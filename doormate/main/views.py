from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from django.contrib.auth import logout
from main.forms import CalendarsForm
from main.models import AuthInfo
from google_auth_oauthlib.flow import Flow
from django.core.exceptions import PermissionDenied
from main.utils import list_calendars, list_events, build_google_service, get_user_profile

# Create your views here.

flow = Flow.from_client_secrets_file(
    './doormate/credentials.json',
    scopes=[
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile', 
    'https://www.googleapis.com/auth/calendar.events.readonly',
    "https://www.googleapis.com/auth/calendar.readonly",
    "openid"],
    redirect_uri='http://127.0.0.1:8000/complete/google-oauth2/')

def google_auth_redirect(request):
    url, state = flow.authorization_url()

    request.session["state"] = state

    return redirect(url)

def google_auth_code_handler(request):
    if "state" not in request.GET or "code" not in request.GET:
        raise PermissionDenied()
    if request.GET["state"] != request.session["state"]:
        raise PermissionDenied()

    # refresh token only returned first time (when user consents) for some accounts
    # there is a way to force return when setting parameters in authorization_url() => prompt=consent&access_type=offline
    token = flow.fetch_token(code=request.GET["code"]) 

    profile = get_user_profile(token["token_type"], token["access_token"])

    google_service = build_google_service(flow.credentials)
    calendars = list_calendars(google_service)
   
    AuthInfo.objects.create(
        email=profile["email"],
        access_token=token["access_token"],
        refresh_token=token["refresh_token"],
        token_type=token["token_type"])

    return render(request, "index.html", {"form": CalendarsForm(calendars)})
