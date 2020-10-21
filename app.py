#!/usr/bin/env python3
import schedule
import time


def collect_readings():
    print("Collecting readings...")


print("Starting Ruuvitag reader")
schedule.every(5).minutes.do(collect_readings)
collect_readings()

while True:
    schedule.run_pending()
    time.sleep(10)
