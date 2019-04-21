#!/usr/bin/env python

from influxdb import InfluxDBClient
import urllib.request
import json
import os
import daemon

url = os.envron['ENGAGE_API_URL']
apiToken = os.environ['EFERGY_API_TOKEN']

with urllib.request.urlopen(url + apiToken):
    data = json.loads(url.read().decode())
    print(data)
