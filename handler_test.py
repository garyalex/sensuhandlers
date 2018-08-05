#!/usr/bin/env python
"""Test Handler for Function devel."""

import sys
import json
import handler_funcs

# users = handler_funcs.getconfig()
# for user in users:
#     print user

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
