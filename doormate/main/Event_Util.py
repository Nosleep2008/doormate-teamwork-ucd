from django.http import HttpResponse
from main.models import Events
from datetime import datetime
import json

def show_event(start_time,end_time):
    start = datetime.strptime(start_time, '%Y-%m-%d %H:%M').astimezone()
    end = datetime.strptime(end_time, '%Y-%m-%d %H:%M').astimezone()
    events = Events.objects.filter(start_time__gte=start).filter(end_time__lte=end).order_by("start_time")
    result={}
    result["events"]=list(events.values())
    return json.dumps(result)

def get_event(time):
    current =  datetime.strptime(time, '%Y-%m-%d %H:%M').astimezone()
    events = Events.objects.filter(start_time__lte=current).filter(end_time__gte=current).order_by("start_time")
    result = {}
    #print(list(events.values()))
    result["events"] = list(events.values())
    return json.dumps(result)

def next_event(time):
    current = datetime.strptime(time, '%Y-%m-%d %H:%M').astimezone()
    result={}
    events=Events.objects.filter(start_time__gte=current).order_by("start_time")
    result["next"]= list(events.values())[0]
    #print(result["next"])
    return json.dumps(result)

def del_event(summary):
    Events.objects.get(summary=summary).delete()
    print("Delete success")



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
    print("Update success")

def old_event(time):
    current = datetime.strptime(time, '%Y-%m-%d %H:%M').astimezone()
    result = {}
    events = Events.objects.filter(end_time__lt=current).order_by("start_time")
    result["old"] = list(events.values())
    return json.dumps(result)