#!/usr/bin/env python3

from influxdb import InfluxDBClient
import urllib.request
import json
import os
import time
import daemon

apiEndpoint = os.environ.get('ENGAGE_API_URL', '')
apiToken = os.environ.get('EFERGY_API_TOKEN', '')


def getData(eUrl, eToken):
    with urllib.request.urlopen(apiEndpoint + apiToken) as url:
        data = json.loads(url.read().decode())
        influxOut = []

        for output in data:
            for values in output['data']:
                for k, v in values.items():
                    valTime = k
                    val = v
            cid = output['cid']
            sid = output['sid']

            influxOut.append(
                {"measurement": "kWm",
                 "tags": {
                     "cid": cid,
                     "sid": sid,
                     },
                 "time": valTime,
                 "fields": {
                     "power": val,
                     },
                 }
            )

    return(influxOut)


def main():
    apiOut = getData(apiEndpoint, apiToken)
    print(json.dumps(apiOut, indent=4))


if __name__ == "__main__":
    main()
