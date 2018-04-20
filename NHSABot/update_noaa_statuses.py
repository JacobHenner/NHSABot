#!/usr/bin/env python3
import logging
from weatheralerts import WeatherAlerts
from .models import NOAA_status

SAMECODE = '034017'

def update_noaa_statuses():
    hudson_county_alerts = WeatherAlerts(samecodes=SAMECODE).alerts
    if hudson_county_alerts:
        for alert in hudson_county_alerts:
            if alert.category == "Met":
                logging.info(f"Weather alert for {alert.areadesc}: {alert.title}")
                existing_alert = NOAA_status.select().where(NOAA_status.url == alert.link)
                if not existing_alert.exists():
                    NOAA_status(severity=alert.severity, summary=alert.summary, status=alert.title, urgency=alert.urgency, effective=alert.effective,
                                expiration=alert.expiration, published=alert.published, updated=alert.updated, areadesc=alert.areadesc, url=alert.link).save()
                else:
                    logging.info("Skipping previously observed alert")
    else:
        logging.info("No NOAA alerts")


if __name__ == "__main__":
    update_noaa_statuses()
