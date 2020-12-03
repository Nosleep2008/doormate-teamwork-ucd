import spidev as SPI
import ST7789
import time
import json
from datetime import datetime

from PIL import Image,ImageDraw,ImageFont
import paho.mqtt.client as mqtt

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 24
bus = 0 
device = 0 

# 240x240 display with hardware SPI:
disp = ST7789.ST7789(SPI.SpiDev(bus, device),RST, DC, BL)

# Initialize library.
disp.Init()

# Clear display.
disp.clear()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("event")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Example: mosquitto_pub -t "event" -m '{"name" : "UCD Meeting", "datetime": "2020-10-10T10:30:00"}'
    print(msg.topic+" "+str(msg.payload))

    payload = json.loads(msg.payload)

    update(payload["name"], payload["datetime"], payload["type"])

def update(name, timestamp, event_type):
    """ Updates screen given name, timestamp and event_type """
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")

    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)

    DO_NOT_DISTURB = "DO NOT DISTURB"
    if event_type == "end":
        STATUS = "Status: Available"
        AVAILABLE = ""
    else:
        STATUS = "Status: %s" % name
        AVAILABLE = "Available at %s" % timestamp.strftime("%H:%M")

    font = ImageFont.truetype("arial.ttf", 18)
    size = font.font.getsize(DO_NOT_DISTURB)
    draw.text((120-size[0][0]//2, 30), DO_NOT_DISTURB, fill = "BLACK", font=font)

    font = ImageFont.truetype("arial.ttf", 12)
    draw.text((disp.width//10, 90),  STATUS, fill="BLACK", font=font)
    draw.text((disp.width//10, 120), AVAILABLE, fill="BLACK", font=font)


    disp.ShowImage(image1,0,0)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    client.loop_forever()
