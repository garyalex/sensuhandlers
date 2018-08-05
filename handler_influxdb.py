#!/usr/bin/env python
"""Handler for sending events to influxdb."""

import sys
import json
import handler_funcs
import os
from influxdb import InfluxDBClient

# Process check
for stdinLine in sys.stdin:
    sendMessage = False
    rawdata = stdinLine
    # print(rawdata)
    jsondata = json.loads(rawdata)
    check = handler_funcs.processcheck(jsondata)
    print "Hostname    : %s" % check.hostname
    print "Status      : %s" % check.status
    print "CheckName   : %s" % check.name
    print "Output      : %s" % check.output
    print "Command     : %s" % check.command
    print "Occurrences : %s" % check.occur

# Send message to influxdb
influxdbhost = os.environ('INFLUX_HOST')
user = os.environ('INFLUX_USER')
password = os.environ('INFLUX_PASS')
dbname = os.environ('INFLUX_DBNAME')
json_body = [
    {
        "measurement": "events",
        "tags": {
            "check_name": check.name,
            "host": "%s" % check.hostname
        },
        "fields": {
            "statuscode": check.statuscode,
            "occurences": check.occur
        }
    }
]

client = InfluxDBClient(influxdbhost, 8086, '', '', dbname)
client.write_points(json_body)
