#!/usr/bin/env python3
import logging
import requests
from bs4 import BeautifulSoup
from .models import Pump

PUMP_IDS = ("35119", "36100", "36101", "27911", "28795", "28974", "35165", "35172", "36098", "35117", "36099", "35324", "35118")

def populate_pumps():

    session = requests.session()
    session.get("https://www.123mc.com/123mc/login.asp?Mobi=N&f=y&1=aufn&87=aufn11776&4=yJKKhQt3WHSpb7AM6hmg1Q%3D%3D")
    session.get("https://www.123mc.com/123mc/map2009.4.asp?pbl=27731")

    for pump_id in PUMP_IDS:
        if not Pump.select().where(Pump.id == pump_id).exists():
            logging.info("Retrieving pump info from https://www.123mc.com/123mc/popalarms.asp?id=%s", pump_id)
            content = session.get("https://www.123mc.com/123mc/popalarms.asp?id=%s" % pump_id).text
            parser = BeautifulSoup(content, 'html.parser')
            name = parser.td.font.next_element.next_element.next_element.next_element.text.split("DSN")[0].strip()
            logging.info("Adding pump %s - %s to database", pump_id, name)
            pump = Pump(id=pump_id,name=name)
            #force_insert needed due to non-autoincrementing primary key
            pump.save(force_insert=True)

if __name__ == "__main__":
    populate_pumps()