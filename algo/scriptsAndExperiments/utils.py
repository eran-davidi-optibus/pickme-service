import csv
import math
from subprocess import call

import googlemaps as gs
import datetime

gmaps = gs.Client(key='AIzaSyBb0Y-hd_A83QFYZmqv451ElvL8sXLp_l4')
today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=1)

def get_geo_from_address(address):
# Geocoding an address
    return gmaps.geocode(address)


def calculate_end_time(start, end, start_time):
    directions_result = gmaps.directions(start,
                                         end,
                                         mode="driving",
                                         departure_time=start_time)
    
    return int(directions_result[0]['legs'][0]['duration_in_traffic']['value']/60)
    
def minute_to_time_of_day(minutes):
    minutes = int(round(minutes))
    hours, minutes = divmod(minutes, 60)
    return '{0}:{1}'.format(str(hours).zfill(2), str(minutes).zfill(2))




x = get_geo_from_address("Begin 23 Tel Aviv")
israel_file_name = "../algo/db/israel.csv"

lat1 = 32.000989
lon1 = 34.759437

lat2 = 32.095176
lon2 = 34.886559

lat3 = 31.479955
lon3 = 32.981741

lat4 = 31.479955
lon4 = 32.981741


point_list = [(lat1, lon1), (lat2, lon2)]

def calc_distance(lon1, lat1, lon2, lat2):

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # output distance in meters

def find_points_for_point_list(point_list):
    f = open(israel_file_name)
    csv_f = csv.reader(f)
    returned_points_min_distance = {}
    returned_points_indices = {}
    returned_points_point = {}
    for row in csv_f:
        lat1 = float(row[1])
        lon1 = float(row[2])
        for ind, point in enumerate(point_list):
            distance = calc_distance(point[0], point[1], lat1, lon1)
            min_distance_until_now = returned_points_min_distance.get(ind, 1000000)
            if distance < min_distance_until_now:
                returned_points_min_distance[ind] = distance
                returned_points_indices[ind] = row[0]
                returned_points_point[ind] = (lat1, lon1)
    return returned_points_indices, returned_points_point

RISHON_IND = 467068
PETAH_IND = 654935

def write_indices_to_in_file(returned_points_indices, source_ind, fname):
    f = open(fname, 'w')
    f.write(str(source_ind) + '\n')
    f.write(str(len(returned_points_indices) / 2) + '\n')
    for i in range(0, len(returned_points_indices), 2):
        f.write(returned_points_indices[i] + '\t' + returned_points_indices[i + 1] + '\n')
    f.close()








