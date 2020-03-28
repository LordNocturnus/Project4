from copy import deepcopy
import numpy as np
import pandas as pd
import os
import sys

flight_num = 10
if 'arrival_modified' not in os.listdir(os.getcwd() + '\\data'):
    os.mkdir(os.getcwd() + f"\\data\\arrival_modified")


arrival_list = os.listdir(os.getcwd() + '\\data\\arrival_processed_2')

for f in range(0, min(len(arrival_list), flight_num)):
    if arrival_list[f] not in os.listdir(os.getcwd() + '\\data\\arrival_modified'):
        os.mkdir(os.getcwd() + f"\\data\\arrival_modified\\{arrival_list[f]}")

    for file in os.listdir(os.getcwd() + f'\\data\\arrival_processed_2\\{arrival_list[f]}'):
        print(f"data\\arrival_processed_2\\{arrival_list[f]}\\{file}")
        data = pd.read_csv(f"data\\arrival_processed_2\\{arrival_list[f]}\\{file}")
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

        data.to_csv(f'data\\arrival_modified\\{arrival_list[f]}\\{file}', index=False)
        del temp
        del data

if 'departure_modified' not in os.listdir(os.getcwd() + '\\data'):
    os.mkdir(os.getcwd() + f"\\data\\departure_modified")


departure_list = os.listdir(os.getcwd() + '\\data\\departure_processed_2')

for f in range(0, min(len(departure_list), flight_num)):
    if departure_list[f] not in os.listdir(os.getcwd() + '\\data\\departure_modified'):
        os.mkdir(os.getcwd() + f"\\data\\departure_modified\\{departure_list[f]}")

    for file in os.listdir(os.getcwd() + f'\\data\\departure_processed_2\\{departure_list[f]}'):
        print(f"data\\departure_processed_2\\{departure_list[f]}\\{file}")
        data = pd.read_csv(f"data\\departure_processed_2\\{departure_list[f]}\\{file}")
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
        del temp
        del data
