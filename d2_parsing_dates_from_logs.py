from datetime import datetime
from datetime import timedelta
import os
import re
import urllib.request

SHUTDOWN_EVENT = "Shutdown initiated"

# prep: read in the logfile
tmp = os.getenv("TMP", "/tmp")
logfile = os.path.join(tmp, "log")
urllib.request.urlretrieve(
    "https://bites-data.s3.us-east-2.amazonaws.com/messages.log", logfile
)

with open(logfile) as f:
    loglines = f.readlines()


def convert_to_datetime(line):
    """
       Extract timestamp from logline and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)
    """
    time_components = re.findall(r"\d+", line)
    timestamp = [int(component) for component in time_components]
    return datetime(*timestamp[0:])


def time_between_shutdowns(loglines):
    """
       Extract shutdown events ("Shutdown initiated") from loglines and
       calculate the timedelta between the first and last one.
       Return this datetime.timedelta object.
    """
    shutdown_events = []
    for line in loglines:
        if SHUTDOWN_EVENT in line:
            shutdown_events.append(convert_to_datetime(line))
    return shutdown_events[1] - shutdown_events[0]


print(time_between_shutdowns(loglines))
