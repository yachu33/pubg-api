import os
import csv
import codecs
import pandas as pd

from flask import Flask, request, current_app
# from flask import request
# from flask import current_app
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    print(__name__, "s")
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
        print(__name__)
        # print(data)
        dataJson = data.to_json(orient='records')
        return dataJson

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
