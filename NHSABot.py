#!/usr/bin/env python3

import time
import os
import requests
import tweepy
from bs4 import BeautifulSoup

def main():
    # Set credentials from environment variables
    CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
    CONSUMER_TOKEN = os.environ.get("CONSUMER_TOKEN")
    USER_KEY = os.environ.get("USER_KEY")
    USER_SECRET = os.environ.get("USER_SECRET")
    # Initiate session
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(USER_KEY, USER_SECRET)
    api = tweepy.API(auth)
    # Manually collected pump IDs
    PUMP_IDS = ("35119", "36100", "36101", "27911", "28795", "28974", "35165", "35172", "36098", "35117", "36099", "35324", "35118")
    # Emulate browser session
    session = requests.session()
    session.get("https://www.123mc.com/123mc/login.asp?Mobi=N&f=y&1=aufn&87=aufn11776&4=yJKKhQt3WHSpb7AM6hmg1Q%3D%3D")
    session.get("https://www.123mc.com/123mc/map2009.4.asp?pbl=27731")

    for pump_id in PUMP_IDS:
        print("https://www.123mc.com/123mc/popalarms.asp?id=%s" % pump_id)
        content = session.get("https://www.123mc.com/123mc/popalarms.asp?id=%s" % pump_id).text
        parser = BeautifulSoup(content, 'html.parser')
        name = make_title(parser.td.font.next_element.next_element.next_element.next_element.text)
        alarm = parser.find("font", color="#FB2222")
        if alarm is not None:
            alarm = alarm.text.split("=>")[1].strip()
            alarm_time = parser.find("font", color="#000000").next_element
            print(name)
            print(alarm)
            print(alarm_time)
            print("Updating Twitter!")
            api.update_status("%s — %s — Duration: %s 💩️" % (name, alarm, alarm_time))
        else:
            print("No alarm")
        print("\n")
        time.sleep(5)
def make_title(title):
    return title.strip()
if __name__ == "__main__":
    main()
