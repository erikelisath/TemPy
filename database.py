import peewee as pwe

db = pwe.SqliteDatabase('database.db')

class BaseModel(pwe.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = pwe.CharField()
    key = pwe.CharField(unique=True)

class SenorData(BaseModel):
    date = pwe.DateTimeField()
    temp = pwe.FloatField()
    humi = pwe.FloatField()
    fkey = pwe.ForeignKeyField(User, backref='data')

def init():
    if db.connect():
        db.create_tables([User, SenorData])
        db.close()
