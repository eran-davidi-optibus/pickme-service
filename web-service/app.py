import gzip
import json
from io import StringIO

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
    def find_rider(self, name):
        global riders
        for rider in riders:
            if rider['name'] == name:
                return rider
        return None

    def post(self):
        data = _get_data()
        global data_updated
        rider = self.find_rider(data['name'])
        if rider is None:
            data_updated = time.time()
            data['id'] = len(riders) + 1
            riders.append(data)
            data = {
                'id': data['id'],
                'text': 'Come back on 7:00 pm to check your route'
            }
            return Response(json.dumps(data), status=200, mimetype='application/json')
        else:
            data = {
                'id': rider['id'],
                'text': 'Come back on 7:00 pm to check your route'
            }
            return Response(json.dumps(data), status=200, mimetype='application/json')


@register_api('/close_route')
class CloseRoute(Resource):
    def post(self):
        data = _get_data()
        print("start post")
        riders_data = []
        # for rider in riders:
        #     rider_data = {}
        #     rider_data['id'] = rider['id']
        #     start_stop = get_geo_from_address(stops[rider['origin_stop_id']-1]['name'])
        #     end_stop = get_geo_from_address(stops[rider['destination_stop_id']-1]['name'])
        #     rider_data['start_lat'] = start_stop[0]['geometry']['location']['lat']
        #     rider_data['start_long'] = start_stop[0]['geometry']['location']['lng']
        #     rider_data['end_lat'] = end_stop[0]['geometry']['location']['lat']
        #     rider_data['end_long'] = end_stop[0]['geometry']['location']['lng']
        #     _, real_start_point = find_points_for_point_list([(rider_data['start_lat'], rider_data['start_long'])])
        #     riders[rider]['origin_stop_id'] = address_from_coor(real_start_point[0])
        #     today = datetime.datetime.today()
        #     tomorrow = today + datetime.timedelta(days=1)
        #     time_string = minute_to_time_of_day(rider['start_time'])
        #     start_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, int(time_string.split(':')[0]), int(time_string.split(':')[1]))
        #     end_time = calculate_end_time(rider['origin_stop_id'], rider['destination_stop_id'], start_time)
        #     rider_data['start_time'] = rider['start_time']
        #     rider_data['end_time'] = end_time
        #     riders_data.append(rider_data)
        #
        # group1 = [riders_data[0], riders_data[1], riders_data[2]]
        # group2 = [riders_data[3], riders_data[4], riders_data[5]]
        #
        # point_list1 = []
        # point_list2 = []
        #
        # for i in group1:
        #     start_stop = (i['start_lat'], i['start_long'])
        #     end_stop = (i['end_lat'], i['end_long'])
        #     point_list1.append(start_stop)
        #     point_list1.append(end_stop)
        #
        # for i in group2:
        #     start_stop = (i['start_lat'], i['start_long'])
        #     end_stop = (i['end_lat'], i['end_long'])
        #     point_list2.append(start_stop)
        #     point_list2.append(end_stop)
        #
        # indices1, _ = find_points_for_point_list(point_list1)
        # indices2, _ = find_points_for_point_list(point_list2)
        #
        # PETAH_IND = 654935
        # HOLON_IND = 35810
        # print('writing files')
        # write_indices_to_in_file(indices1, PETAH_IND, 'points1.in')
        # write_indices_to_in_file(indices2, HOLON_IND, 'points2.in')
        # print("running A*")
        # path1 = run_astar('points1.in')
        # path2 = run_astar('points2.in')
        # a=1
        #
        #

        data = {
            'data_updated': data_updated,
            'status': RideStatus.pending.name,
            'riders': riders,
            'buses': buses,
            'stops': stops
        }
        return Response(json.dumps(data), status=200, mimetype='application/json')


@register_api('/reset')
class Reset(Resource):
    def post(self):
        init()
        return 'ok'


if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0')
