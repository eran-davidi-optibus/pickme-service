import gzip
import json
from StringIO import StringIO

from files import from_json_file
from flask import Flask, request
from flask_restful import abort, Api, Resource

app = Flask(__name__)
api = Api(app)

riders = None
buses = None
stops = None


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

        return {
            'status': 'pending',
            'riders': riders,
            'buses': buses,
            'stops': stops
        }


@register_api('/riders/add')
class AddRider(Resource):
    def post(self):
        data = _get_data()
        if data['name'] != 'Moshe':
            abort(403)
            return

        data['id'] = len(riders) + 1
        riders.append(data)
        return {
            'id': data['id']
        }


if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0')
