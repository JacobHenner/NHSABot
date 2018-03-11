#!/usr/bin/env python3
import os
import logging
import tweepy
import inflect
from .models import Pump, Status

def tweet_statuses():
    # Set credentials from environment variables
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
    CONSUMER_TOKEN = os.environ.get("CONSUMER_TOKEN")
    USER_KEY = os.environ.get("USER_KEY")
    USER_SECRET = os.environ.get("USER_SECRET")
    # Initiate session
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(USER_KEY, USER_SECRET)
    api = tweepy.API(auth)

    for status in Status.select().where(Status.processed==False):
        logging.info("Evaluating: " + status.pump.name)
        if status.status == "No alarm":
            previous_status = Status.select().where(Status.pump == status.pump, Status.id != status.id).order_by(Status.id.desc())
            if previous_status.exists():
                # Status has been switched to no alarm after period of different status. 
                message = "The pump at %s is no longer reporting an alarm condition.\n\nIt had been reporting one since %s, which was %s ago." % (status.pump.name, previous_status.get().timestamp.strftime("%H:%M:%S on %B %d, %Y"), format_timedelta(status.timestamp - previous_status.get().timestamp))
                logging.info("Tweeting: %s" % message)
                api.update_status(message)
            else:
                # No alarm, but there are no records for comparsion. Do not tweet.
                logging.info("No alarm - no prior records for this pump.")
        else:
            # There is an alarm status.
            message = "The pump at %s has started to report %s.\n\nThis status was first observed at %s." % (status.pump.name, status.status,status.timestamp.strftime("%H:%M:%S on %B %d, %Y"))
            logging.info("Tweeting: %s" % message)
            api.update_status(message)
            
        status.processed = True
        status.save()

def format_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    p = inflect.engine()
    string = ""
    string = string + "%d %s," % (days, p.plural("day", days)) if days != 0 else ""
    string = string + "%d %s," % (hours, p.plural("hour", hours)) if hours != 0 else ""
    string = string + "%d %s" % (minutes, p.plural("minute", minutes)) if minutes != 0 else ""
    return string

if __name__=="__main__":
    tweet_statuses()