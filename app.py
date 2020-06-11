import os
import csv
import codecs
import pandas as pd

from flask import Flask
from flask import request
from flask import current_app
from flask_cors import cross_origin

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def hello():
        return 'Hello, World!'
    

    @app.route('/get_data', methods=['GET'])
    @cross_origin()
    def get_data():
        maps = request.values.get('map')
        weapon = request.values.get('weapon')
        rank = request.values.get('rank')
        time = request.values.get('time')
        
        with current_app.open_resource('kill5000.csv', "rb") as csv_file:
            data = pd.read_csv(csv_file)
            # & (kill_pd["level"] == level)
            if maps :
                data = data.loc[data["map"] == maps]
            if weapon :
                data = data.loc[data["killed_by"] == weapon]
            if time :
                data = data.loc[data["time"] <= float(time)]
            if rank :
                data = data.loc[data["rank"] == rank]
            print(data)
            dataJson = data.to_json(orient='records')
            return dataJson
    return app