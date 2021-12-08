import peewee as pwe

db = pwe.SqliteDatabase('database.db')

class BaseModel(pwe.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = pwe.CharField()
    key = pwe.CharField(unique=True)

class SensorData(BaseModel):
    date = pwe.DateTimeField()
    temp = pwe.FloatField()
    humi = pwe.FloatField()
    fkey = pwe.ForeignKeyField(User, backref='data')

def init():
    if db.connect():
        db.create_tables([User, SensorData])
        db.close()
    else:
        print('Cannot connect to database!')

def testdata():
    if db.connect():
        try:
            user = User(name='erik', key='erik')
            user.save()
        except:
            print('Test User Exists')
        db.close()
