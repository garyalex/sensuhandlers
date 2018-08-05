#!/usr/bin/python
"""Handler for sending slack alerts from sensu."""

import sys
import json
import handler_funcs
import argparse
import os
from slackclient import SlackClient

# Setup our arguments
parser = argparse.ArgumentParser()
parser.add_argument("channel", help="Channel to send to", type=str)
args = parser.parse_args()

# Set our variables from commandline arguments
channel = args.channel

# Constants
slack_token = os.environ("SLACK_TOKEN")

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

    # Condition logic
    if check.occur == 1 or check.action != "create" or (check.occur % 60) == 0:
        sendMessage = True

    if sendMessage:
        msgsubject = "%s alert - %s - on - %s" % (check.status,
                                                  check.name,
                                                  check.hostname)
        msgbody = """
        *COMMAND:* %s
        *OUTPUT:* %s
        *OCCUR:* %s
        """ % (check.command, check.output, check.occur)
        msgText = "*%s*\n%s" % (msgsubject, msgbody)
        # Setup slack client
        sc = SlackClient(slack_token)
        # Send PB message
        sc.api_call(
            "chat.postMessage",
            channel="#%s" % channel,
            text="%s" % msgText,
            asuser="false",
            username="Monitor",
            icon_url="http://bit.ly/2ninRvQ"
        )
