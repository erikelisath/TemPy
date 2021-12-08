from flask import request
from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, pprint
import datetime as dt

from database import User, SensorData

# Schema for correct data pushing
class TempSchema(Schema):
    temp = fields.Float(
            required=True,
            error_message={'required': 'Temperature is required.'}
    )
    humi = fields.Float(
            required=True,
            error_message={'required': 'Humidity is required.'}
    )
    date = fields.DateTime(
            format='iso',
            error_message={'invalid': 'Only ISO format: YYYY-MM-DDThh:mm:ss.sss'}
    )

# TemPy Rest Api
class TemPyRest(Resource):
    # GET
    def get(self, id):
        user = User.select().where(User.key == id)

        if user.exists():
            return {'request': f'Hello {user.get().name}'}
        else:
            return {'request': 'No User with this key aviable.'}

    # PUT
    def put(self, id):
        print(f'PUT - for ID: {id}')
        req_data = None
        temp_schema = TempSchema()
        user = User.select().where(User.key == id)

        if user.exists():
            try:
                reqjson = request.get_json(force = True)
                req_data = temp_schema.load(reqjson)
            except ValidationError as err:
                pprint(err)
                return {'error': err.messages}, 422

            print('REQUEST DATA:', req_data)
            if 'date' not in req_data:
                req_data['date'] = dt.datetime.now()

            sensor_data = SensorData(
                            temp=req_data['temp'],
                            humi=req_data['humi'],
                            date=req_data['date'],
                            fkey = id)
            if sensor_data.save():
                return {'success': 'Data saved.'}
            else:
                return {'failed': 'Data was not saved.'}

        else:
            return {'error': 'User not exists.'}
