### Sensu Handlers

Custom handlers for [Sensu](https://sensu.io/).

These will take an event from Sensu from standard input, and process it, sending it out via Email or Slack, or sending it to InfluxDB.

Email sending has a configurable contacts list (A YAML file). See the example provided.
This will send email based on alert name, hostname or group.


### Notes
- Email requires environment variable SENSU_FROM_EMAIL to be set
- User email alert config is set in /usr/local/etc/contacts.yaml - see the example file included
- For sending InfluxDB events set the following environment variables INFLUX_HOST, INFLUX_USER, INFLUX_PASS, INFLUX_DBNAME
- For sending Slack messages, get a Slack token and set the environme nt variable SLACK_TOKEN