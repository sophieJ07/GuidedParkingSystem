# for testing Arduino Cloud connection (user end)

import time
import logging
import asyncio
import numpy as np
import sys
sys.path.append("lib")
import nest_asyncio
nest_asyncio.apply()
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = b"574903a4-ba42-41c2-aacb-ef41b219597f"
SECRET_KEY = b"GFaB79rQ4n3y!lI#Q!QOLRGL0"

def logging_func():
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )

def on_switch_changed_1(client, value):
    print("spot changed1: ", value)

def on_switch_changed_2(client, value):
    print("spot changed2: ", value)

def on_switch_changed_3(client, value):
    print("spot changed3: ", value)

def on_switch_changed_4(client, value):
    print("spot changed4: ", value)

def on_switch_changed_5(client, value):
    print("spot changed5: ", value)

if __name__ == '__main__':
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
    client.register("spot1", on_write=on_switch_changed_1)
    client.register("spot2", on_write=on_switch_changed_2)
    client.register("spot3", on_write=on_switch_changed_3)
    client.register("spot4", on_write=on_switch_changed_4)
    client.register("spot5", on_write=on_switch_changed_5)
    print("finished registration, starting client")

    client.start()
