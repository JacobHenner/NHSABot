import datetime
import peewee

db = peewee.SqliteDatabase("nhsa.db")

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Pump(BaseModel):
    name = peewee.CharField()
    def __str__(self):
        return self.name

class Status(BaseModel):
    pump = peewee.ForeignKeyField(Pump, backref="statuses")
    timestamp = peewee.DateTimeField(default=datetime.datetime.now)
    status = peewee.CharField()
    processed = peewee.BooleanField(default=False)
    def __str__(self):
        return "%s: %s - %s" % (self.pump.name, self.status, self.timestamp)

db.connect()
db.create_tables([Pump, Status])
db.close()