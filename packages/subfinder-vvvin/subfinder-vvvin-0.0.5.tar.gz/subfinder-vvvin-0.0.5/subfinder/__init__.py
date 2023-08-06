import pickle
from math import radians, cos, sin, asin, sqrt
import reverse_geocoder as rg
import textdistance


class subfinder:
    def __init__(self):
        f = open('./subfinder/suburbs.dat', 'rb')
        lst = pickle.load(f)
        self.sub_info = lst[0]
        self.sub_same = lst[1]
        f.close()

    def get_key(self, value):
        return [k for k, v in self.sub_info.items() if v == value]

    def CompareUrbanArea(self, urban_area, lng, lat):
        all_urban_key = self.get_key(urban_area)
        if all_urban_key:
            nearest = float('inf')
            nearest_city = None
            for area in all_urban_key:
                dlon = self.sub_info[area]["lng"] - lng
                dlat = self.sub_info[area]["lat"] - lat
                dis = ((dlon**2) + (dlat**2))**0.5
                if dis < nearest:
                    nearest = dis
                    nearest_city = area
            return nearest_city
        else:
            return None

    def CalSimilarity(self, suburb, lng, lat):
        pending_lst = []
        for key in self.sub_same:
            sim = textdistance.jaro_winkler.similarity(key, suburb)
            if sim > 0.7:
                pending_lst.append(key)
        nearest = float('inf')
        nearest_city = None
        for area in pending_lst:
            dlon = self.sub_info[area]["lng"] - lng
            dlat = self.sub_info[area]["lat"] - lat
            dis = ((dlon**2) + (dlat**2))**0.5
            if dis < nearest:
                nearest = dis
                nearest_city = area
        return nearest_city

    def GetPlace(self, lat, lng):
        coordinates = [lat, lng]
        address = rg.search(coordinates, mode=1)
        suburb = address[0]["name"]
        state = address[0]["admin1"]
        urban_area = address[0]["admin2"]

        if suburb in self.sub_same:
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
        else:
            if urban_area:
                new_suburb = self.CompareUrbanArea(urban_area, lng, lat)
                if not new_suburb:
                    best_match = self.CalSimilarity(suburb, lng, lat)
                    if best_match:
                        result = dict()
                        result["suburb"] = best_match
                        result["state"] = state
                        result["city"] = self.sub_info[best_match]["statistic_area"]
                        return result
                    return None
                else:
                    result = dict()
                    result["suburb"] = urban_area
                    result["state"] = state
                    result["city"] = self.sub_info[new_suburb]["statistic_area"]
                    return result
            else:
                best_match = self.CalSimilarity(suburb, lng, lat)
                if best_match:
                    result = dict()
                    result["suburb"] = best_match
                    result["state"] = state
                    result["city"] = self.sub_info[best_match]["statistic_area"]
                    return result
                else:
                    return None
