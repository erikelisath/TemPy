import peewee as pwe
import os.path as op
import datetime as dt
from shutil import copy

db = pwe.SqliteDatabase(None)

class BaseModel(pwe.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = pwe.CharField(unique=True)

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

    if type(db) is pwe.SqliteDatabase:
        # check if database file exists
        if op.isfile(app.config['DATABASE']):
            # create backup of database
            copy(app.config['DATABASE'],
                dt.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')+'_'+app.config['DATABASE'])
            app.logger.info('Found existing database, create backup.')

        else:
            # create database with tables
            if db.connect():
                db.create_tables([User, Device, SensorData]) # will  create tables with 'IF NOT EXISTS'
                app.logger.info(f'Create database "{app.config["DATABASE"]}" with tables.')
                db.close()
            else:
                app.logger.error('Can not connect to database!')

        # when development modus is set create test data
        if app.config['ENV'] == 'development':
            testdata(app)

def testdata(app):
    if db.connect():
        try:
            test_user = User.create(name='Tester')
            device = Device.create(key='test', info='ESP-12E', environment='Living room', fuser=test_user)
            sensordata = SensorData.insert_many([
                {'temp':'21.0', 'humi':'33.0', 'date':'2021-01-01T10:10:10', 'fdevice':device},
                {'temp':'22.0', 'humi':'35.0', 'date':'2021-01-01T10:11:10', 'fdevice':device},
                {'temp':'23.0', 'humi':'37.0', 'date':'2021-01-01T10:12:10', 'fdevice':device}
            ]).execute()
            app.logger.debug('Create test data.')
        except:
            app.logger.debug('Test data already exists!')
        db.close()
