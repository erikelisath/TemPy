from flask import render_template, request, g
from tempy.db import User, Device, SensorData
import datetime as dt
import statistics
from time import process_time
import subprocess


def index():
    return render_template('index.html')

def start():
    query = Device.select()
    return render_template('start.html', devices=query)


def show(key=None):
    print('hello')
    # show only data when key exists
    if Device.get_or_none(Device.key == key):
        query = None
        date = []
        temp = []
        humi = []
        device = Device.get(Device.key == key)
        stats = {'records': get_sensor_data(key).count()}

        # POST method
        if request.method == 'POST':
            # button 'last 24h'
            if request.form.get('name') == 'all':
                g.name = 'all'
                query = get_query(key, 24)

            # button 'last 24h (less)'
            elif request.form.get('name') == 'less':
                g.name = 'less'
                query = get_query(key, 24, True)

            # button 'last 2h'
            elif request.form.get('name') == 'time':
                g.name = 'time'
                query = get_query(key, 2)

        # GET method
        elif request.method == 'GET':
            g.name = 'time'
            query = get_query(key, 2)

        date = [data.date for data in query]
        temp = [data.temp for data in query]
        humi = [data.humi for data in query]

        # fill stats
        if temp and humi:
            stats['mean_temp'] = round(statistics.mean(temp), 2)
            stats['mean_humi'] = round(statistics.mean(humi), 2)

        if date:
            stats['last_recd'] = date[-1]
        else:
            stats['last_recd'] = get_last_sensor_data(key).date

        return render_template(
                    'show.html',
                    device=device,
                    stats=stats,
                    date=date,
                    temp=temp,
                    humi=humi
                    )

    # if the key not exists
    else:
        return render_template('none.html', key=key)


def raw(key=None):
    if Device.get_or_none(Device.key == key):
        query = SensorData.select().join(Device).where(Device.key == key)
        return render_template('raw.html', key=key, sensor_data=query)
    else:
        return render_template('none.html', key=key)


# return sensor data from database
def get_sensor_data(key, hours=None):
    if hours:
        # will return the data from (now - hours)
        return (SensorData.select()
                                .join(Device)
                                .where(
                                    (Device.key == key)
                                    & (SensorData.date
                                        >= (dt.datetime.now()
                                        - dt.timedelta(hours=hours)).isoformat()
                                    )
                                )
                                .order_by(SensorData.date))
    else:
        return (SensorData.select()
                                .join(Device)
                                .where(Device.key == key)
                                .order_by(SensorData.date))


def get_last_sensor_data(key):
    return (SensorData.select()
                            .join(Device)
                            .where(Device.key == key)
                            .order_by(SensorData.date.desc())
                            .get())

# custom jinja filter
def str_to_datetime(str):
    return dt.datetime.fromisoformat(str).strftime('%b. %d, %y - %H:%M:%S')


def get_query(key, hours, less=False):
    if less:
        query = get_sensor_data(key, hours)
        ldata = []

        if query:
            for count, element in enumerate(query, 1):
                if count %10 == 0:
                    ldata.append(element)

            if ldata:
                if query[-1].date != ldata[-1].date:
                    ldata.append(query[-1]) # the last sensor data will be not lost
                query = ldata

        return query
    else:
        return get_sensor_data(key, hours)


def ping_sensor(key):
    param = '-c' # if windows, use -n
    host = Device.select().where(Device.key == key).get()

    if host.ip_addr is not None:
        command = ['ping', param, '1', '-w 1', host.ip_addr]
        if subprocess.call(command, stdout=subprocess.DEVNULL) == 0:
            return 'green' # online

    return 'red' # offline
