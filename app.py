#!/usr/bin/env python3
import schedule
import time
from ruuvitag_sensor.ruuvi import RuuviTagSensor
import ruuvitag_sensor.log
import json
import requests

get_data_timeout_sec = 60

print("Loading config...")
config = json.loads(open("config.json").read())
macs = config["sensors"].keys()

print(f"Collecting measurements from {len(macs)} sensors")
print(f"Sending measurements to {config['collector_url']}")


def get_name(mac):
    if mac in config["sensors"]:
        return config["sensors"][mac]
    return mac


def collect_readings():
    print("Collecting readings...")
    try:
        datas = RuuviTagSensor.get_data_for_sensors(macs, get_data_timeout_sec)
        measurements = []
        for mac, data in datas.items():
            data["mac"] = mac
            data["name"] = get_name(mac)
            measurements.append(data)

        body = {"measurements": measurements}
        requests.post(config["collector_url"], json=body)
        print(f"Sent {len(measurements)} measurements to collector")
    except Exception as e:
        print("Failed to collect and send readings")
        print(e)


print("Starting Ruuvitag reader")
schedule.every(config["interval"]).seconds.do(collect_readings)
collect_readings()

while True:
    schedule.run_pending()
    time.sleep(10)
