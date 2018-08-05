### Sensu Handlers
Python Sensu Handlers


### Notes
- Email requires environment variable SENSU_FROM_EMAIL to be set
- User email alert config is set in /usr/local/etc/contacts.yaml - see the example file included
- For sending InfluxDB events set the following environment variables INFLUX_HOST, INFLUX_USER, INFLUX_PASS, INFLUX_DBNAME
- For sending Slack messages, get a Slack token and set the environme nt variable SLACK_TOKEN