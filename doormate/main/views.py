from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import JsonResponse
import requests
from django.contrib.auth import logout
from main.forms import CalendarsForm
from main.models import AuthInfo, Events
from google_auth_oauthlib.flow import Flow
from django.core.exceptions import PermissionDenied
from main.utils import list_calendars, list_events, build_google_service, get_user_profile
from datetime import datetime
import telepot
import time


# Create your views here.
TOKEN = '1300396895:AAF2b0Ync9M5uLmZTYtrihJ0aQaUbvL-s9Q'
bot = telepot.Bot(TOKEN)

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

    if AuthInfo.objects.count() == 1:
        auth_info = AuthInfo.objects.first()
        auth_info.email = profile["email"]
        auth_info.access_token = profile["access_token"]
        auth_info.refresh_token = profile["refresh_token"]
        auth_info.token_type = profile["token_type"]
    else:
   
        AuthInfo.objects.create(
            email=profile["email"],
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            token_type=token["token_type"])

    return render(request, "index.html", {"form": CalendarsForm(calendars)})

def index(request):
    return render(request, "index.html")

def insert_event(request,summary,name,start_time,end_time,status):
    start = datetime.strptime(start_time,'%Y-%m-%d %H:%M').astimezone()
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M').astimezone()

    Events.objects.create(
        summary=summary,
        name=name,
        start_time=start,
        end_time=end,
        status=status
    )

    return HttpResponse("Insert success")

def show_event(request,start_time,end_time):
    start = datetime.strptime(start_time, '%Y-%m-%d %H:%M').astimezone()
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M').astimezone()
    events = Events.objects.filter(start_time__gte=start).filter(end_time__lte=end).order_by("start_time")
    #print(events)
    result={}
    result["events"]=list(events.values())
    return JsonResponse(result)

def get_event(request,time):
    current =  datetime.strptime(time, '%Y-%m-%d %H:%M').astimezone()
    events = Events.objects.filter(start_time__lte=current).filter(end_time__gte=current).order_by("start_time")
    result = {}
    #print(list(events.values()))
    result["events"] = list(events.values())
    return JsonResponse(result)

def next_event(request,time):
    current = datetime.strptime(time, '%Y-%m-%d %H:%M').astimezone()
    result={}
    events=Events.objects.filter(start_time__gte=current).order_by("start_time")
    result["next"]= list(events.values())[0]
    #print(result["next"])
    return JsonResponse(result)

def del_event(request,summary):
    Events.objects.get(summary=summary).delete()
    return  HttpResponse("Delete success")


def update_event(request,summary,name,start_time,end_time,status):
    events = Events.objects.filter(summary=summary)
    start = datetime.strptime(start_time, '%Y-%m-%d %H:%M').astimezone()
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M').astimezone()
    if events.exists():
        event = Events.objects.get(summary=summary)
        event.name = name
        event.start_time = start
        event.end_time = end
        event.status = status
        event.save()
    else:
        Events.objects.create(
            summary=summary,
            name=name,
            start_time=start,
            end_time=end,
            status=status
        )
    return HttpResponse("Update success")

def telegram_message(request,chat_id, text):
    print(bot.getMe())
    bot.sendMessage(chat_id, text)