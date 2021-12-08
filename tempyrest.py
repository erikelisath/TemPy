from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, pprint

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

class TemPyRest(Resource):
    def get(self, id):
        print(id)
        return {'success': 'ok'}

    def put(self, id):
        print(id)
        return {'success': 'ok'}
