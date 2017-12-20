import googlemaps as gs
from datetime import datetime

gmaps = gs.Client(key='AIzaSyBb0Y-hd_A83QFYZmqv451ElvL8sXLp_l4')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
def address_from_coor(coor):
    return gmaps.reverse_geocode(coor)

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("ben gurion 12 holon",
                                     "begin 23 tel aviv",
                                     mode="driving",
                                     departure_time=now)

a=1