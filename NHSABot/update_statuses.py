#!/usr/bin/env python3
import logging
from datetime import datetime
from .models import Pump, Status
from bs4 import BeautifulSoup
import requests

session = requests.session()
session.get("https://www.123mc.com/123mc/login.asp?Mobi=N&f=y&1=aufn&87=aufn11776&4=yJKKhQt3WHSpb7AM6hmg1Q%3D%3D")
session.get("https://www.123mc.com/123mc/map2009.4.asp?pbl=27731")

def update_statuses():
    for pump in Pump.select():
        id = pump.id
        logging.info("Retrieving status of pump #%d, %s" % (id, pump.name))
        content = session.get("https://www.123mc.com/123mc/popalarms.asp?id=%s" % id).text
        parser = BeautifulSoup(content, 'html.parser')
        try:
            alarm = parser.find("font", color="#FB2222")
        except AttributeError:
            logging.exception("Failed to retrieve status of pump #%d, %s" % (id, pump.name))
            date = datetime.now().isoformat()
            with open(date + ".err",'w') as errorlog:
                errorlog.write(content)
                logging.info("Response content available in %s.err for debugging." % date)
            continue
        if alarm is not None:
            status = alarm.text.split("=>")[1].strip()
            logging.info("Alarm condition: %s" % status)
            update_status(pump, status)
        else:
            logging.info("No alarm condition")
            update_status(pump, "No alarm")

def update_status(pump, status):
    last_status = Status.select().where(Status.pump == pump).order_by(Status.id.desc())
    if not last_status.exists() or last_status.get().status != status:
        logging.info("Pump status differs from last entry, updating database")
        Status(pump=pump, status=status).save()

if __name__ == "__main__":
    update_statuses()