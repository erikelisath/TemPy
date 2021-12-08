from flask import Flask
from flask_restful import Api

import tempydash
import tempyrest
import database


app = Flask(__name__)
api = Api(app)


app.add_url_rule('/', view_func=tempydash.index)
app.add_url_rule('/show/<key>', view_func=tempydash.show)
api.add_resource(tempyrest.TemPyRest, '/<string:id>')

if __name__ == '__main__':
    database.init()
    database.testdata()
    app.run(debug=True)
