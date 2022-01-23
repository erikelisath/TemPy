import os
from flask import Flask
from flask_restful import Api


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    app.config.from_mapping(
        SECRET_KEY='something_has_secrets_here',
        DATABASE='database.db'
    )

    # import modules
    from . import dash
    from . import rest
    from . import db

    # add urls and resources
    app.add_url_rule('/', view_func=dash.index)
    app.add_url_rule('/start', view_func=dash.start)
    app.add_url_rule('/show/<key>', view_func=dash.show, methods=['GET', 'POST'])
    app.add_url_rule('/raw/<key>', view_func=dash.raw)
    api.add_resource(rest.TemPyRest, '/<string:key>')
    app.jinja_env.filters['strdate'] = dash.str_to_datetime
    app.jinja_env.globals['ping'] = dash.ping_sensor
    app.jinja_env.globals['last_sensor_data'] = dash.get_last_sensor_data

    # init database
    db.init(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
