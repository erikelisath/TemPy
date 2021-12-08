from flask import render_template
from database import User, SensorData

#@app.route('/')
def index():
    query = User.select()
    return render_template('index.html', keys=query)

def show(key=None):
    query = SensorData.select().where(SensorData.fkey == key)
    print(len(query))
    return render_template('show.html', key=key, sensor_data=query)
