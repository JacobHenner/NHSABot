#!/usr/bin/env python3
import os
import logging
import tweepy
import inflect
from .models import Pump_status, NOAA_status

# Set credentials from environment variables
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
CONSUMER_TOKEN = os.environ.get("CONSUMER_TOKEN")
USER_KEY = os.environ.get("USER_KEY")
USER_SECRET = os.environ.get("USER_SECRET")
# Initiate session
auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
auth.set_access_token(USER_KEY, USER_SECRET)
twitter_api = tweepy.API(auth)


def tweet_pump_statuses():
    for status in Pump_status.select().where(Pump_status.processed == False):
        logging.info("Evaluating: %s", status.pump.name)
        if status.status == "No alarm":
            previous_status = Pump_status.select().where(Pump_status.pump == status.pump,
                                                         Pump_status.id != status.id).order_by(Pump_status.id.desc())
            if previous_status.exists():
                # Status has been switched to no alarm after period of different status.
                message = "The pump at %s is no longer reporting an alarm condition.\n\nIt had been reporting one since %s, which was %s ago." % (
                    status.pump.name, previous_status.get().timestamp.strftime("%H:%M:%S on %B %d, %Y"), _format_timedelta(status.timestamp - previous_status.get().timestamp))
                logging.info("Tweeting: %s", message)
                twitter_api.update_status(message)
            else:
                # No alarm, but there are no records for comparsion. Do not tweet.
                logging.info("No alarm - no prior records for this pump.")
        else:
            # There is an alarm status.
            message = "The pump at %s has started to report %s.\n\nThis status was first observed at %s." % (
                status.pump.name, status.status, status.timestamp.strftime("%H:%M on %B %d, %Y"))
            logging.info("Tweeting: %s", message)
            twitter_api.update_status(message)

        status.processed = True
        status.save()


def tweet_noaa_statuses():
    for status in NOAA_status.select().where(NOAA_status.processed == False):
        message = "%s.\n\n@NWS: \"%s\"" % (status.status, status.summary)
        if status.severity != "Minor" and status.severity != "Unknown":
            logging.info("Tweeting: %s", message)
            twitter_api.update_status(message)
        else:
            logging.info("Not tweeting due to insufficient severity: %s", message)
        status.processed = True
        status.save()


def _format_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    p = inflect.engine()
    string = ""
    string = string + \
        "%d %s, " % (days, p.plural("day", days)) if days != 0 else ""
    string = string + \
        "%d %s, " % (hours, p.plural("hour", hours)) if hours != 0 else ""
    string = string + \
        "%d %s" % (minutes, p.plural("minute", minutes)
                  ) if minutes != 0 else ""
    return string


if __name__ == "__main__":
    tweet_pump_statuses()
    tweet_noaa_statuses()
