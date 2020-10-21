#!/bin/bash
set -eux

sudo apt-get install python3 python3-pip bluez bluez-hcidump
pip3 install -r requirements.txt
