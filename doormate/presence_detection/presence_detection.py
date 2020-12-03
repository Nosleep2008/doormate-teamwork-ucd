import time
import json
from datetime import datetime
import telepot

import paho.mqtt.client as mqtt

PRESENT_DEVICES_CONFIDENCE = {}
CHATS = {}

TOKEN = '1300396895:AAF2b0Ync9M5uLmZTYtrihJ0aQaUbvL-s9Q'
bot = telepot.Bot(TOKEN)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.message_callback_add('event', on_message_event)
    client.message_callback_add('monitor/raspberrypi/#', on_message_presence)
    client.subscribe("#")

def on_message_event(client, userdata, msg):
    payload = json.loads(msg.payload)
    print(msg.payload)

    for name in PRESENT_DEVICES_CONFIDENCE:
        if PRESENT_DEVICES_CONFIDENCE[name] > 80:
            time = datetime.strptime(payload["datetime"], "%Y-%m-%dT%H:%M:%S")
            message_device(name, time)

def on_message_presence(client, userdata, msg):
    print(msg.payload)
    if msg.payload.decode() not in ["online", "offline"]:
        payload = json.loads(msg.payload)
        name = payload["name"]
        confidence = payload["confidence"]
        PRESENT_DEVICES_CONFIDENCE[name] = confidence

def message_device(device_name, end_time):
    bot.sendMessage(CHATS[device_name], "Don't make noise, a meeting is ongoing until " + end_time.strftime("%H:%M"))

def load_devices():
    filehandle = open("./known_static_addresses", "r")
    for device in filehandle:
        device_name = device.split()[1]
        chat_id = device.split()[2][1:]
        PRESENT_DEVICES_CONFIDENCE[device_name] = 0
        CHATS[device_name] = chat_id
    

if __name__ == "__main__":
    load_devices()
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect("localhost", 1883, 60)

    client.loop_forever()
