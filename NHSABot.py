#!/usr/bin/env python3
import logging
from NHSABot import populate_pumps, update_pump_statuses, update_noaa_statuses, tweet_pump_statuses, tweet_noaa_statuses

logging.basicConfig(handlers=[logging.StreamHandler(), logging.FileHandler("NHSABot.log")],level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    populate_pumps()
    update_pump_statuses()
    update_noaa_statuses()
    tweet_pump_statuses()
    tweet_noaa_statuses()
