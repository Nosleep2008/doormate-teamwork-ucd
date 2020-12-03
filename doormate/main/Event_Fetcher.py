import json
import time
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt
import pytz
from apscheduler.schedulers.background import BlockingScheduler

#from paho import mqtt
from main.Event_Util import old_event, show_event, update_event
from main.utils import list_events


class event_fetcher:
    service = ''
    calendar = 'primary'
    client = ''

    # time_limit is the lifetime of event_fetcher
    def __init__(self, google_service, scheduler: BlockingScheduler, calendar="primary", time_limit=60 * 6 * 144):
        self.service = google_service
        self.calendar = calendar
        self.scheduler = scheduler
        self.update_database()  # initial database
        self.client = self.establish_message_broker()  # establish connection with mqtt server
        # start to watching new events from google (every 2 min) and refresh display (every 10s)
        # self.run(time_limit)

    '''
    def run(self, time_limit):
        while time_limit > 3600:
            time.sleep(10)
            self.display_current_event()  # every 10 sec
            if time_limit % 12 == 0:  # every 2 min
                self.update_database()
            if time_limit % 3600 == 0:  # every 10 hour
                self.clear_passed_events()
            time_limit = time_limit - 1
    '''

    def get_events_from_api(self):
        res = list_events(self.service, self.calendar)
        return res["items"]

    def clear_passed_events(self):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        old_event(now)

    def display_current_event(self, summary, end_time):
        print("Sending current event...")
        event = {"name": summary, "datetime": end_time}
        self.publish_message(json.dumps(event))

    def update_database(self):
        events_list = self.get_events_from_api()
        print("Updating Events DB...")
        first = True
        for event in events_list:
            print("Adding event to DB")
            summary = event["summary"]
            start_time = datetime.strptime(event["start"]["dateTime"], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc)
            end_time = datetime.strptime(event["end"]["dateTime"], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc)
            status = event["status"]
            if first:
                first = False

                message_datetime = start_time
                if start_time < datetime.utcnow().astimezone(pytz.utc):
                    message_datetime = datetime.now() + timedelta(seconds=5)

                self.scheduler.add_job(
                    self.display_current_event,
                    id="display_current_event",
                    replace_existing=True,
                    trigger='date',
                    run_date=message_datetime,
                    args=(summary, end_time))

            update_event("r", summary, summary, start_time, end_time, status)

    def establish_message_broker(self):
        client = mqtt.Client(protocol=3)
        client.connect(host="127.0.0.1", port=1883, keepalive=60)
        return client

    def publish_message(self, event):
        # Publish MQTT message for parameter event
        if not self.client == '':
            self.client.publish(topic="event", payload=event, qos=1)
