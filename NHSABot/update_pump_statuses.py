#!/usr/bin/env python3
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from .models import Pump, Pump_status

session = requests.session()
session.get("https://www.123mc.com/123mc/login.asp?Mobi=N&f=y&1=aufn&87=aufn11776&4=yJKKhQt3WHSpb7AM6hmg1Q%3D%3D")
session.get("https://www.123mc.com/123mc/map2009.4.asp?pbl=27731")

def update_pump_statuses():
    for pump in Pump.select():
        pump_id = pump.id
        logging.info("Retrieving status of pump #%d, %s", pump_id, pump.name)
        content = session.get("https://www.123mc.com/123mc/popalarms.asp?id=%s" % pump_id).text
        parser = BeautifulSoup(content, 'html.parser')
        try:
            alarm = parser.find("font", color="#FB2222")
        except AttributeError:
            logging.exception("Failed to retrieve status of pump #%d, %s", pump_id, pump.name)
            date = datetime.now().isoformat()
            with open(date + ".err", 'w') as errorlog:
                errorlog.write(content)
                logging.info("Response content available in %s.err for debugging.", date)
            continue
        if alarm is not None:
            status = alarm.text.split("=>")[1].strip()
            logging.info("Alarm condition: %s", status)
            update_pump_status(pump, status)
        else:
            logging.info("No alarm condition")
            update_pump_status(pump, "No alarm")

def update_pump_status(pump, status):
    last_status = Pump_status.select().where(Pump_status.pump == pump).order_by(Pump_status.id.desc())
    if not last_status.exists() or last_status.get().status != status:
        logging.info("Pump status differs from last entry, updating database")
        Pump_status(pump=pump, status=status).save()

if __name__ == "__main__":
    update_pump_statuses()
