import gzip
import json
from StringIO import StringIO

import time

from enum import Enum

from files import from_json_file
from flask import Flask, request, Response
from flask_restful import abort, Api, Resource
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

riders = None
buses = None
stops = None
data_updated = None
RideStatus = Enum('RideStatus', 'pending closed')


def _get_data():
    if request.content_encoding == 'gzip':
        fp = StringIO(request.data)
        with gzip.GzipFile(fileobj=fp) as gzipfile:
            jsonstr = gzipfile.read()
        return jsonstr
    return json.loads(request.data)


def register_api(url):
    def wrapper(cls):
        api.add_resource(cls, url)
        return cls

    return wrapper


def init():
    global riders, buses, stops
    riders = from_json_file('./data/riders.json')
    buses = from_json_file('./data/buses.json')
    stops = from_json_file('./data/stops.json')


@register_api('/riders/status')
class RidersStatus(Resource):
    def get(self):
        global data_updated
        if data_updated is None:
            data_updated = time.time()
        data = {
            'data_updated': data_updated,
            'status': RideStatus.pending.name,
            'riders': riders,
            'buses': buses,
            'stops': stops
        }
        return Response(json.dumps(data), status=200, mimetype='application/json')


@register_api('/riders/add')
class AddRider(Resource):
    def post(self):
        data = _get_data()
        if data['name'] != 'Moshe':
            abort(403)
            return

        global data_updated
        data_updated = time.time()
        data['id'] = len(riders) + 1
        riders.append(data)
        return {
            'id': data['id']
        }


if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0')
