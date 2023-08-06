import pickle
from math import radians, cos, sin, asin, sqrt
import reverse_geocoder as rg


class subfinder:
    def __init__(self):
        f = open('suburbs.dat', 'rb')
        lst = pickle.load(f)
        self.sub_info = lst[0]
        self.sub_same = lst[1]
        f.close()

    def GetPlace(self, lat, lng):
        coordinates = [lat, lng]
        address = rg.search(coordinates, mode=1)
        suburb = address[0]["name"]
        state = address[0]["admin1"]

        if len(self.sub_same[suburb]) == 1:
            return self.sub_info[suburb]["statistic_area"]
        else:
            nearest = float('inf')
            nearest_city = None
            for name in self.sub_same[suburb]:
                dlon = self.sub_info[name]["lng"] - lng
                dlat = self.sub_info[name]["lat"] - lat
                dis = ((dlon**2) + (dlat**2))**0.5
                if dis < nearest:
                    nearest = dis
                    nearest_city = name
            result = dict()
            result["suburb"] = suburb
            result["state"] = state
            result["city"] = self.sub_info[nearest_city]["statistic_area"]
            return result
