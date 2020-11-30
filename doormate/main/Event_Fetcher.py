import time
from datetime import datetime
#from paho import mqtt
from doormate.main.Event_Util import old_event, show_event, update_event
from doormate.main.utils import list_events
import paho.mqtt.client as mqtt

class event_fetcher:
    service = ''
    calender = 'primary'
    client = ''

    # time_limit is the lifetime of event_fetcher
    def __init__(self, google_service, calender="primary", time_limit=60 * 6 * 144):
        self.service = google_service
        self.calender = calender
        self.update_database(self)  # initial database
        self.client = self.establish_message_broker()  # establish connection with mqtt server
        # start to watching new events from google (every 2 min) and refresh display (every 10s)
        # self.run(time_limit)
        self.client.disconnect()

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
        res = list_events(self.service, self.calender)
        return res["items"]

    def clear_passed_events(self):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        old_event(now)

    def display_current_event(self, hour=1):
        now = datetime.datetime.now()
        offset = datetime.timedelta(hours=2)
        further_hours = (now + offset).strftime('%Y-%m-%d %H:%M:%S')
        events = show_event(now, further_hours)  # return json information , only need the first one (currently)
        self.publish_message(events[0])  # pass the first one to message broker function

    def update_database(self):
        events_list = self.get_events_from_api()
        for event in events_list:
            summary = event["summary"]
            start_time = event["start"]["datetime"]
            end_time = event["end"]["datetime"]
            status = event["status"]
            update_event("r", summary, summary, start_time, end_time, status)

    def establish_message_broker(self):
        client = mqtt.Client(protocol=3)
        client.connect(host="127.0.0.1", port=1883, keepalive=60)
        return client

    def publish_message(self, event):
        # Publish MQTT message for parameter event
        if not self.client == '':
            self.client.publish(topic="event", payload=event, qos=0)
