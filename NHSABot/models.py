import datetime
import peewee

db = peewee.SqliteDatabase("nhsa.db")

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Status(BaseModel):
    timestamp = peewee.DateTimeField(default=datetime.datetime.now)
    status = peewee.CharField()
    processed = peewee.BooleanField(default=False)

class Pump(BaseModel):
    name = peewee.CharField()
    def __str__(self):
        return self.name

class Pump_status(Status):
    pump = peewee.ForeignKeyField(Pump, backref="Pump_statuses")
    def __str__(self):
        return "%s: %s - %s" % (self.pump.name, self.status, self.timestamp)

class NOAA_status(Status):
    severity = peewee.CharField()
    summary = peewee.TextField()
    urgency = peewee.CharField()
    effective = peewee.DateTimeField()
    expiration = peewee.DateTimeField()
    published = peewee.DateTimeField()
    updated = peewee.DateTimeField()
    areadesc = peewee.CharField()
    url = peewee.CharField()
    def __str__(self):
        return self.title

db.connect()
db.create_tables([Pump, Pump_status, NOAA_status])
db.close()