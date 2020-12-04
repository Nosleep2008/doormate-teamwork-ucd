import json
from datetime import datetime
import pytz

from django.http import HttpResponse

from main.models import Events, Calendars


def show_event(start_time,end_time):
    events = Events.objects.filter(start_time__gte=start_time).filter(end_time__lte=end_time).order_by("start_time")
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
    if events.exists():
        event = Events.objects.get(summary=summary)
        event.name = name
        event.start_time = start_time
        event.end_time = end_time
        event.status = status
        event.save()
    else:
        Events.objects.create(
            summary=summary,
            name=name,
            start_time=start_time,
            end_time=end_time,
            status=status
        )
    print("Update success")

def old_event(time):
    current = datetime.strptime(time, '%Y-%m-%d %H:%M').astimezone()
    result = {}
    events = Events.objects.filter(end_time__lt=current).order_by("start_time")
    result["old"] = list(events.values())
    return json.dumps(result)

def get_calendars():
    return [c.calendar_id for c in Calendars.objects.all()]

def order_events_for_calendars(calendars):
    indices = [0] * len(calendars)

    num_events = sum([len(c) for c in calendars])

    events = []

    while sum(indices) < num_events:
        next_event = None
        min_time = None
        calendar_idx = None
        for i in range(len(calendars)):
            if indices[i] < len(calendars[i]):
                event = calendars[i][indices[i]]
                next_time = datetime.strptime(event["start"]["dateTime"], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc)
                if min_time == None or min_time > next_time:
                    min_time = next_time
                    next_event = event
                    calendar_idx = i

        events.append(next_event)
        indices[calendar_idx] += 1

    return events
