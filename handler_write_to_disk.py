#!/usr/bin/python

import sys

# variables
f = open("/var/log/sensu/handler_log_output.log", "a+")

for stdinLine in sys.stdin:
    f.write("%s\n" % stdinLine)
