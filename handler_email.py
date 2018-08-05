#!/usr/bin/env python
"""Handler for sending email alerts from sensu."""

import sys
import json
import argparse
import handler_funcs

# Setup our arguments
parser = argparse.ArgumentParser()
parser.add_argument("--email", "-e", help="Email to override", type=str)
args = parser.parse_args()

# Set our variables from commandline arguments
singleemail = args.email

# variables
# statuses = ["OK", "WARN", "CRIT", "UNKN"]
# colors = ["green", "orange", "red", "grey"]

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
        if not singleemail:
            # get our taglist
            taglist = handler_funcs.gentaglist(check.sublist, check.name,
                                               check.hostname)
            # get our email list
            emaillist = handler_funcs.getemaillist(taglist)
            # Send emails
            for emailaddress in emaillist:
                handler_funcs.sendemail(emailaddress, check)
        else:
            handler_funcs.sendemail(singleemail, check)
