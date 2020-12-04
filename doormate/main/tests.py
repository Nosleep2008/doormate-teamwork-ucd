from django.test import TestCase
from main.Event_Util import order_events_for_calendars
from datetime import datetime, timedelta
import pytz

# Create your tests here.

class Event_Util(TestCase):

    def test_given_events_from_calendars_then_events_ordered(self):
        calendar1 = [{"summary": 1 ,"start": {"dateTime": (datetime.utcnow() + timedelta(hours=1)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}}]
        calendar2 = [{"summary": 2, "start": {"dateTime": (datetime.utcnow() + timedelta(hours=2)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}}]
        calendar3 = [{"summary": 3, "start": {"dateTime": (datetime.utcnow() + timedelta(hours=3)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}}]
        events = order_events_for_calendars([calendar1, calendar2, calendar3])

        self.assertEqual(events[0]["summary"], 1)
        self.assertEqual(events[1]["summary"], 2)
        self.assertEqual(events[2]["summary"], 3)

    def test_given_events_from_multiple_calendars_then_events_ordered(self):
        calendar1 = [
                {"summary": 1 ,"start": {"dateTime": (datetime.utcnow() + timedelta(hours=1)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}},
                {"summary": 3 ,"start": {"dateTime": (datetime.utcnow() + timedelta(hours=3)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}}
            ]
        calendar2 = [
                {"summary": 2, "start": {"dateTime": (datetime.utcnow() + timedelta(hours=2)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}},
                {"summary": 4, "start": {"dateTime": (datetime.utcnow() + timedelta(hours=4)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}}
            ]
        calendar3 = [{"summary": 5, "start": {"dateTime": (datetime.utcnow() + timedelta(hours=5)).astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}}]
        events = order_events_for_calendars([calendar3, calendar2, calendar1])

        self.assertEqual(events[0]["summary"], 1)
        self.assertEqual(events[1]["summary"], 2)
        self.assertEqual(events[2]["summary"], 3)
        self.assertEqual(events[3]["summary"], 4)
        self.assertEqual(events[4]["summary"], 5)
