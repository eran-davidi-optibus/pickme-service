from files import from_json_file
from flask import Flask, request
from flask.ext.restful import abort, Api, Resource

app = Flask(__name__)
api = Api(app)

riders = None


def register_api(url):
    def wrapper(cls):
        api.add_resource(cls, url)
        return cls

    return wrapper


def init():
    global riders
    riders = from_json_file('./riders.json')


@register_api('/riders/status')
class RidersStatus(Resource):
    def get(self):

        return {
            'status': 'pending',
            'riders': riders
        }


if __name__ == '__main__':
    init()
    app.run(debug=True)
