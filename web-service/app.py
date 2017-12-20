from files import from_json_file
from flask import Flask
from flask.ext.restful import abort, Api, Resource

app = Flask(__name__)
api = Api(app)

riders = None
buses = None
stops = None


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


if __name__ == '__main__':
    init()
    app.run(debug=True)
