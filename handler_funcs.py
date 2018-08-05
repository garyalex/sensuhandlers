# handler_funcs
"""Functions needed for sensu handlers."""

import yaml
import dpath.util
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class sensucheck(object):
    """
    A check object for sensu.

    Attributes:
        name: A string representing the check name.
        hostname: host that the check is coming from
        command: command that was run to check current status
        output: command output
        occur: number of occurences of this status
        action: action (create, resolve)
        status: status (Critical, Warning, OK, Unknown)
        statuscode: output code of check (0, 1, 2, 3)
    """

    def __init__(self, name, hostname, command, output, occur, action, status,
                 color, sublist, statuscode):
        """Return a Check object."""
        self.name = name
        self.hostname = hostname
        self.command = command
        self.output = output
        self.occur = occur
        self.action = action
        self.status = status
        self.color = color
        self.sublist = sublist
        self.statuscode = statuscode


def getconfig():
    """Get config from file and return object."""
    # Open file and read config
    with open("/usr/local/etc/contacts.yaml", 'r') as stream:
        try:
            users = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return users


def printconfig():
    """Print our config and exit."""
    users = getconfig()

    for user in users:
        name = dpath.util.get(user, '/user')
        email = dpath.util.get(user, '/email')
        tags = dpath.util.get(user, '/tags')
        print "NAME: %s EMAIL: %s TAGS: %s" % (name, email, tags)
    return


def getemaillist(taglist):
    """Get email address list."""
    emaillist = []
    """Get list of email addresses to send to based on tag list supplied."""
    if not isinstance(taglist, list):
        # Not a list so raise exception
        raise TypeError('taglist supplied is not a list.')
    else:
        # Get our contacts config
        users = getconfig()
        # Outer loop over provided tags
        for checktag in taglist:
            # Inner loop over users
            for user in users:
                email = dpath.util.get(user, '/email')
                tags = dpath.util.get(user, '/tags')
                if checktag in tags:
                    emaillist.append(email)
    # Sort and dedupe list
    emaillist = sorted(set(emaillist))
    # Return list
    return emaillist


def sendemail(emailaddress, check):
    """Send email."""
    # Constants
    emailfrom = os.environ['SENSU_FROM_EMAIL']
    emailsubject = "%s alert - %s - on - %s" % (check.status,
                                                check.name,
                                                check.hostname)

    # Create message container - the correct MIME type
    # is multipart/alternative
    msg = MIMEMultipart('alternative')
    msg['Subject'] = emailsubject
    msg['From'] = emailfrom
    msg['To'] = emailaddress

    # Create the body of the message (a plain-text and an HTML version).
    text = "COMMAND: %s\nOUTPUT : %s" % (check.command, check.output)
    html = """\
    <html>
      <head></head>
      <body>
        <h3 style="color:%s">%s</h3>
        <p><b>COMMAND:</b> %s<br>
           <b>OUTPUT :</b><br>
           %s
        </p>
      </body>
    </html>
    """ % (check.color, emailsubject, check.command, check.output)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via smtp2go SMTP server.
    s = smtplib.SMTP('mail.smtp2go.com', 2525)
    s.sendmail(emailfrom, emailaddress, msg.as_string())
    s.quit()


def gentaglist(sublist, checkname, hostname):
    """Generate a tag list for passing to tag checking."""
    # Constants
    taglist = ["all"]
    # remove domain names from hostname
    hostname = hostname.split('.')[0]
    # Build our taglist
    taglist += sublist
    taglist.append(hostname)
    taglist.append(checkname)
    # Return our list
    return taglist


def processcheck(jsondata):
    """Get data from json and assign to check object."""
    # Constants
    statuses = ["OK", "WARN", "CRIT", "UNKN"]
    colors = ["green", "orange", "red", "grey"]
    # Get our individual values
    hostname = dpath.util.get(jsondata, '/client/name')
    checkName = dpath.util.get(jsondata, '/check/name')
    sublist = dpath.util.get(jsondata, '/client/subscriptions')
    try:
        checkcommand = dpath.util.get(jsondata, '/check/command')
    except KeyError:
        checkcommand = "None"
    try:
        checkoutput = dpath.util.get(jsondata, '/check/output')
    except KeyError:
        checkoutput = "None"
    action = dpath.util.get(jsondata, '/action')
    occurrences = int(dpath.util.get(jsondata, '/occurrences'))
    checkoutput = checkoutput.strip(' \t\n\r')
    statuscode = int(dpath.util.get(jsondata, '/check/status'))
    status = statuses[statuscode]
    color = colors[int(dpath.util.get(jsondata, '/check/status'))]
    # Now assign our class
    check = sensucheck(name=checkName, hostname=hostname, command=checkcommand,
                       output=checkoutput, action=action, occur=occurrences,
                       status=status, color=color, sublist=sublist,
                       statuscode=statuscode)
    return check
