import peewee as pwe

db = pwe.SqliteDatabase('database.db')

class BaseModel(pwe.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = pwe.CharField()

class Device(BaseModel):
    key = pwe.CharField(unique=True)
    info = pwe.CharField()
    environment = pwe.CharField()
    fuser = pwe.ForeignKeyField(User, backref='owner')

class SensorData(BaseModel):
    date = pwe.DateTimeField()
    temp = pwe.FloatField()
    humi = pwe.FloatField()
    fdevice = pwe.ForeignKeyField(Device, backref='sensor')

def init():
    if db.connect():
        db.create_tables([User, Device, SensorData])
        db.close()
    else:
        print('Cannot connect to database!')

def testdata():
    if db.connect():
        try:
            test_user = User.create(name='Erik')
            device = Device.create(key='test', info='ESP-12E', environment='Living room', fuser=test_user)
        except:
            print('Test User Exists')
        db.close()
