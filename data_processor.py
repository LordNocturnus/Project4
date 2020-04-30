from copy import deepcopy
import numpy as np
import pandas as pd
import os

flight_num = 1000
if 'arrival_modified' not in os.listdir(os.getcwd() + '\\data'):
    os.mkdir(os.getcwd() + f"\\data\\arrival_modified")

arrival_list = os.listdir(os.getcwd() + '\\data\\arrival_flights')

data_arrival = []
loitering = []
removed = []

for f in range(0, len(arrival_list)):
    if arrival_list[f] not in os.listdir(os.getcwd() + '\\data\\arrival_modified'):
        os.mkdir(os.getcwd() + f"\\data\\arrival_modified\\{arrival_list[f]}")

    for file in os.listdir(os.getcwd() + f'\\data\\arrival_flights\\{arrival_list[f]}'):

        data = pd.read_csv(f"data\\arrival_flights\\{arrival_list[f]}\\{file}", dtype={'icao24': str,
                                                                                       'destination': str,
                                                                                       'callsign': str,
                                                                                       'flight_id': str})
        #data["geo_vs_baro_alt"] = data["geoaltitude"] - data["altitude"]
        temp = deepcopy(data)
        temp = temp.shift()
        data["geo_change"] = temp["geoaltitude"] - data["geoaltitude"]
        data["alt_change"] = temp["altitude"] - data["altitude"]
        data["heading_change"] = temp["track"] - data["track"]
        data.loc[data["heading_change"] <= -180, ["heading_change"]] += 360
        data.loc[data["heading_change"] >= 180, ["heading_change"]] -= 360
        data["geo_track"] = np.degrees(np.arctan2(temp["longitude"] - data["longitude"],
                                                  temp["latitude"] - data["latitude"])) + 180
        temp = deepcopy(data)
        temp = temp.shift()
        data["geo_track_change"] = temp["geo_track"] - data["geo_track"]
        data.loc[data["geo_track_change"] <= -180, ["geo_track_change"]] += 360
        data.loc[data["geo_track_change"] >= 180, ["geo_track_change"]] -= 360

        temp = deepcopy(data)
        temp = temp.shift()
        data["vel_change"] = temp["groundspeed"] - data["groundspeed"]
        data["usefull"] = np.full(len(data), True)
        data["usefull"][0:2] = False
        temp = [data.std(axis=0, skipna=True, numeric_only=True), data.mean(axis=0, skipna=True, numeric_only=True)]
        for c in temp[0].index.values:
            data.loc[temp[1][c] - temp[0][c] * 3 > data[c], "usefull"] = False
            data.loc[temp[1][c] + temp[0][c] * 3 < data[c], "usefull"] = False
        if f < flight_num:
            data.to_csv(f'data\\arrival_modified\\{arrival_list[f]}\\{file}', index=False)
        data_arrival.append(data)
        if abs(sum(data['geo_track_change'][2:])) >= 360:
            loitering.append(file[:-4])
        removed.append((len(data) - len(data[data['usefull']])) / len(data))
        print(
            f"data\\arrival_flights\\{arrival_list[f]}\\{file}: {(len(data) - len(data[data['usefull']])) / len(data)}")
        del temp
        del data

'''if 'departure_modified' not in os.listdir(os.getcwd() + '\\data'):
    os.mkdir(os.getcwd() + f"\\data\\departure_modified")

departure_list = os.listdir(os.getcwd() + '\\data\\departure_flights')

temp = pd.read_csv(f"data\\departure_flights\\2FPLF\\2FPLF_3122.csv", dtype={'icao24': str,
                                                                           'destination': str,
                                                                           'callsign': str,
                                                                           'flight_id': str})
data_limit_departure = pd.DataFrame([temp.min(axis=0, skipna=True), temp.max(axis=0, skipna=True)])
data_mean_departure = []

for f in range(0, min(len(departure_list), flight_num)):
    if departure_list[f] not in os.listdir(os.getcwd() + '\\data\\departure_modified'):
        os.mkdir(os.getcwd() + f"\\data\\departure_modified\\{departure_list[f]}")

    for file in os.listdir(os.getcwd() + f'\\data\\departure_flights\\{departure_list[f]}'):
        print(f"data\\departure_flights\\{departure_list[f]}\\{file}")
        data = pd.read_csv(f"data\\departure_flights\\{departure_list[f]}\\{file}", dtype={'icao24': str,
                                                                                           'destination': str,
                                                                                           'callsign': str,
                                                                                           'flight_id': str})
        data["geo_vs_baro_alt"] = data["geoaltitude"] - data["altitude"]
        temp = deepcopy(data)
        temp = temp.shift()
        data["geo_change"] = temp["geoaltitude"] - data["geoaltitude"]
        data["alt_change"] = temp["altitude"] - data["altitude"]
        data["heading_change"] = temp["track"] - data["track"]
        data.loc[data["heading_change"] <= -180, ["heading_change"]] += 360
        data.loc[data["heading_change"] >= 180, ["heading_change"]] -= 360
        data["geo_track"] = np.degrees(np.arctan2(temp["longitude"] - data["longitude"],
                                                  temp["latitude"] - data["latitude"])) + 180
        temp = deepcopy(data)
        temp = temp.shift()
        data["geo_track_change"] = temp["geo_track"] - data["geo_track"]
        data.loc[data["geo_track_change"] <= -180, ["geo_track_change"]] += 360
        data.loc[data["geo_track_change"] >= 180, ["geo_track_change"]] -= 360

        data.to_csv(f'data\\departure_modified\\{departure_list[f]}\\{file}', index=False)
        data_limit_departure = pd.DataFrame(
            [data_limit_departure.min(axis=0, skipna=True, numeric_only=True),
             data_limit_departure.max(axis=0, skipna=True, numeric_only=True),
             data.min(axis=0, skipna=True, numeric_only=True),
             data.max(axis=0, skipna=True, numeric_only=True)])
        data_mean_departure.append(data.mean(axis=0, skipna=True, numeric_only=True))
        del temp
        del data'''

data_arrival = pd.concat(data_arrival)
data_limit_arrival = pd.DataFrame([data_arrival[data_arrival["usefull"]].std(axis=0, skipna=True, numeric_only=True),
                                   data_arrival[data_arrival["usefull"]].mean(axis=0, skipna=True, numeric_only=True)])

'''data_mean_departure = pd.DataFrame(data_mean_departure)
data_limit_departure = pd.DataFrame([data_limit_departure.min(axis=0, skipna=True, numeric_only=True),
                                     data_mean_departure.mean(axis=0, skipna=True, numeric_only=True),
                                     data_limit_departure.max(axis=0, skipna=True, numeric_only=True)])'''

data_limit_arrival.to_csv(f'data\\arrival_modified\\limits.csv', index=False)

f = open("data\\turnaround.list", "w")
for l in loitering:
    f.write(l + "\n")
f.close()

print((len(data_arrival) - len(data_arrival[data_arrival['usefull']])) / len(data_arrival))
# data_limit_departure.to_csv(f'data\\departure_modified\\limits.csv', index=False)
