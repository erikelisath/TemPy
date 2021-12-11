from flask import render_template
from database import User, Device, SensorData

#@app.route('/')
def index():
    query = Device.select()
    return render_template('index.html', devices=query)

def show(key=None):
    query = SensorData.select().join(Device).where(Device.key == key)
    print(len(query))
    return render_template('show.html', key=key, sensor_data=query)
