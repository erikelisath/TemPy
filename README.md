# TemPy
Small temperature display application with dashboard and REST API, implemented with python library Flask. Can be used in combination with ESP32 boards as sensors, see the TemPySensor Arduino script.

**Requirements**

* Flask
* FlaskRESTful
* peewee
* marshmallow

**Run flask application**

1. `export FLASK_APP=tempy` - TemPy application, for the terminal environment
2. `export FLASK_ENV=development` - optional, running the app in development mode with debugging
3. `flask run` - run the TemPy app, optional `--host=0.0.0.0` for externally visible server (public)

## TemPyDash

Overview of available sensor data.

## TempPyRest
Small REST API application through which the data is pushed. The data is written to the database via HTTP PUT request if the key is valid and the JSON format of the request is correct. The temperature and humidity are mandatory, the date is optional.

**Example**

```bash
curl 127.0.0.1:5000/kj2 -X PUT -d '{"temp": "23.3", "humi": "33"}' -H "Content-Type: application/json"
# {'success': 'Data saved.'}
```
**Explanation**

`127.0.0.1:5000` - network address with port, depending where the service is running  
`/kj2` - stored key, each sensor must have its own key  
`-X PUT` - HTTP request method for requested payload  
`-d '{"temp": "23.3", "humi": "33"}'` - data attribute in JSON format.  
`-H "Content-Type: application/json"` - needed header to provide the client with the actual content type in the body (JSON format)  
`{'success': 'Data saved.'}` - the response will be in JSON format, data successfully stored in database

**Available data attributes**

`temp` - requested, float type, Temperature  
`humi` - requested, float type, Humidity  
`date` - optional, date time ISO format, Date with Time
`pres` - *not realized*, Air Pressure

## Database

Tables
```
| user |
| id | name |

| device |
| id | key | info | environment | fuser |

| sensordata |
| id | date | temp | humi | fdevice |
```

## Status

Work in progress!

**Open to implement** 

- [ ] Data attribute: air pressure
- [ ] better GET request
- [ ] manage keys in dashboard
