#!/bin/bash

echo 'Installing lib files...'
#

echo 'Installing lib files...'
if ! command -v circup &> /dev/null
then
    pip install setuptools
    pip install circup
fi
circup install neopixel adafruit_lsm6ds adafruit_register adafruit_hid adafruit_motor adafruit_hcsr04 adafruit_dht 
