#!/usr/bin/env python3

from influxdb import InfluxDBClient
import argparse
import urllib.request
import json
import os
import datetime
import csv

apiEndpoint = os.environ.get('ENGAGE_API_URL', '')
apiToken = os.environ.get('EFERGY_API_TOKEN', '')


def getData(eUrl, eToken):
    """get data from egage api"""
    if eUrl == '' or eToken == '':
        print("Enviroment is not setup")
        exit(1)

    with urllib.request.urlopen(eUrl + eToken) as url:
        data = json.loads(url.read().decode())

    return(data)


def parseApi(data):
    """parse engage api data and format for influxdb"""
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


def importReport(reportFile, apiOut):
    """parse csv reports downloaded from engage site"""
    reportList = []
    for line in csv.DictReader(open(reportFile)):
        date_time = datetime.datetime.strptime(line['Timestamp'],
                                               '%Y-%m-%d %H:%M:%S')

        del line['Timestamp']
        for k, v in line.items():
            if v != '':
                for data in apiOut:
                    if data['sid'] in k:
                        sid = data['sid']
                        cid = data['cid']

                reportList.append(
                    {"measurement": "kWm",
                     "tags": {
                         "cid": cid,
                         "sid": sid,
                         },
                     "time": date_time.isoformat(),
                     "fields": {
                         "power": int(v.rstrip('.0')),
                         },
                     }
                )

    return(reportList)


def insetData(jsonData, ibHost, ibPort):
    """insert json into influxdb"""
    inclient = InfluxDBClient(
        host=ibHost,
        port=ibPort,
        username='admin',
        password='password'
        )
    inclient.switch_database('efergy')
    inclient.write_points(jsonData)


def main():
    startTime = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        description='Simple Python script to pull from engage API \
                    and store data in influxdb'
    )
    parser.add_argument(
        "-i, --import", action="store", type=str,
        dest="importCSV",
        help='import csv downloaded from engage"'
    )
    parser.add_argument(
        "-d, --debug", action="store_true",
        dest="debug",
        help='output json to be inserted to influx, but do not insert"'
    )

    cliarg = parser.parse_args()

    try:
        cliarg.importCSV
    except NameError:
        cliarg.importCSV = None

    apiOut = getData(apiEndpoint, apiToken)

    if cliarg.importCSV is None:
        apiIBData = parseApi(apiOut)
        if cliarg.debug is True:
            jsonData = json.dumps(apiIBData, indent=4)
            print(jsonData)
        else:
            insetData(apiIBData, "efergy-influx", 8086)
    else:
        csvIBData = importReport(cliarg.importCSV, apiOut)
#        jsonData = json.dumps(csvIBData, indent=4)
        if cliarg.debug is True:
            jsonData = json.dumps(csvIBData, indent=4)
            print(jsonData)
        else:
            insetData(csvIBData, "127.0.0.1", 8087)
    endTime = datetime.datetime.now()
    runTime = endTime - startTime
    print("Finished run at: " + str(endTime) +
          " run took " + str(int(runTime.total_seconds() * 1000)) + "ms")


if __name__ == "__main__":
    main()
