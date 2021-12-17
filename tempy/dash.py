from flask import render_template, request, g
from tempy.db import User, Device, SensorData
import datetime as dt


def index():
    query = Device.select()
    return render_template('index.html', devices=query)


def show(key=None):
    # show only data when key exists
    if Device.get_or_none(Device.key == key):
        data = []
        query = SensorData.select().join(Device).where(
            Device.key == key
            and SensorData.date >= (dt.datetime.now() - dt.timedelta(hours=24))
        ) # sensor data for the last 24h
        device = Device.get(Device.key == key)

        # POST method
        if request.method == 'POST':
            if request.form.get('view') == 'ALL':
                g.view = 'ALL'
                return render_template('show.html', device=device, sensor_data=query)

            elif request.form.get('view') == 'LESS':
                g.view = 'LESS'
                for count, element in enumerate(query, 1):
                    if count %10 == 0:
                        data.append(element)
                return render_template('show.html', device=device, sensor_data=data)

            elif request.form.get('time') == '2h':
                g.time = '2h'
                query = SensorData.select().join(Device).where(
                    Device.key == key
                    and SensorData.date >= (dt.datetime.now() - dt.timedelta(hours=2))
                )
                return render_template('show.html', device=device, sensor_data=query)


        # GET method
        elif request.method == 'GET':
            g.view = 'ALL'
            return render_template('show.html', device=device, sensor_data=query)

    else:
        return render_template('none.html', key=key)


def raw(key=None):
    if Device.get_or_none(Device.key == key):
        query = SensorData.select().join(Device).where(Device.key == key)
        return render_template('raw.html', key=key, sensor_data=query)
    else:
        return render_template('none.html', key=key)
