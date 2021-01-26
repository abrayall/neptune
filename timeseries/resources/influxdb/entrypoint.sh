#!/bin/bash
set -m
influxd run &
sleep 5

influx setup -b neptune -o neptune -u neptune -p neptune@12345 -t Ku-vr2Vu70U47XRsUhNBRB2LoCkoSAQNEEzFc8Mncw72MLvQwaQf6ct0QERwzbN7Mhy8F16apCkkR5Obg0zhaw== -f
fg 1
