from flask import render_template, request, g
from tempy.db import User, Device, SensorData
import datetime as dt
import statistics


def index():
    query = Device.select()
    return render_template('index.html', devices=query)


def show(key=None):
    # show only data when key exists
    if Device.get_or_none(Device.key == key):
        query = None
        date = []
        temp = []
        humi = []
        device = Device.get(Device.key == key)
        stats = {'records': len(get_sensor_data(key))}

        # POST method
        if request.method == 'POST':
            # button ALL
            if request.form.get('view') == 'ALL':
                g.view = 'ALL'
                query = get_sensor_data(key, 24)

            # button LESS
            elif request.form.get('view') == 'LESS':
                g.view = 'LESS'
                query = get_sensor_data(key, 24)
                ldata = []

                if query:
                    for count, element in enumerate(query, 1):
                        if count %10 == 0:
                            ldata.append(element)

                    if query[-1].date != ldata[-1].date:
                        ldata.append(query[-1]) # the last sensor data will be not lost
                    query = ldata

            # button 2h
            elif request.form.get('time') == '2h':
                g.time = '2h'
                query = get_sensor_data(key, 2)

        # GET method
        elif request.method == 'GET':
            g.view = 'ALL'
            query = get_sensor_data(key, 24)

        for data in query:
            date.append(data.date)
            temp.append(data.temp)
            humi.append(data.humi)

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
