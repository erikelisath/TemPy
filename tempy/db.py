import peewee as pwe

db = pwe.SqliteDatabase(None)

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

def init(app):
    db.init(app.config['DATABASE'])
    if db.connect():
        db.create_tables([User, Device, SensorData])
        app.logger.debug(f'Create database "{app.config["DATABASE"]}" with tables')
        db.close()
    else:
        app.logger.error('Can not connect to database!')

def testdata():
    if db.connect():
        try:
            test_user = User.create(name='Erik')
            device = Device.create(key='test', info='ESP-12E', environment='Living room', fuser=test_user)
            sensordata = SensorData.create(temp='23.0', humi='33.0', date='2021-01-01T10:10:10', fdevice=device)
        except:
            print('Can not create test data')
            #current_app.logger.debug('Test data already exists')
        db.close()
