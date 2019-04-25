#!/usr/bin/env python3

from influxdb import InfluxDBClient
import argparse
import urllib.request
import json
import os
import datetime
import daemon
import csv


def getData(eUrl, eToken):
    with urllib.request.urlopen(eUrl + eToken) as url:
        data = json.loads(url.read().decode())
        influxOut = []

        for output in data:
            for values in output['data']:
                for k, v in values.items():
                    ksec = int(k) / 1000
                    valTime = datetime.datetime.fromtimestamp(int(ksec))
                    val = v
            cid = output['cid']
            sid = output['sid']

            influxOut.append(
                {"measurement": "kWm",
                 "tags": {
                     "cid": cid,
                     "sid": sid,
                     },
                 "time": valTime.isoformat(),
                 "fields": {
                     "power": val,
                     },
                 }
            )

    return(influxOut)


def importReport(reportFile):
    reportList = []
    for line in csv.DictReader(open(reportFile)):
        reportList.append(line)

    return(reportList)

def insetData(jsonData):
    inclient = InfluxDBClient(
        host='127.0.0.1',
        port=8087,
        username='admin',
        password='password'
        )
    inclient.switch_database('efergy')
    inclient.write_points(jsonData)


def main():
    # Set options
    parser = argparse.ArgumentParser(
        description='Simple Python script pull from engage API \
                    and store data in influxdb'
    )
    parser.add_argument(
        "-i, --import", action="store", type=str,
        dest="importCSV",
        help='import csv downloaded from engage"'
    )

    cliarg = parser.parse_args()

    try:
        cliarg.importCSV
    except NameError:
        cliarg.importCSV = None

    if cliarg.importCSV is None:
        apiEndpoint = os.environ.get('ENGAGE_API_URL', '')
        apiToken = os.environ.get('EFERGY_API_TOKEN', '')
        apiOut = getData(apiEndpoint, apiToken)

    else:
        apiOut = importReport(cliarg.importCSV)
    jsonData = json.dumps(apiOut, indent=4)
    print(jsonData)
    # insetData(apiOut)


if __name__ == "__main__":
    main()
