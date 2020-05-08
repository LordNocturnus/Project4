import os
import pandas as pd
import numpy as np
from copy import deepcopy
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import hsv_to_rgb
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def scaling(data, limits, width=2):
    for c in limits.columns:
        if c in data.columns:
            data[c] = (data[c] - limits[c][1]) / (limits[c][0] * 6) * width
    return data


# N integers to N distinguishable color_range function, Note: works but recommend manually selecting color_range if possible
def color_range(n, colorshift):
    # ret = np.array([0, 0, 0])
    start = colorshift
    h = start
    s = 100
    v = 100
    step = (360 - start) / (n - 1)
    ret = np.zeros((n, 3), dtype=np.float)
    for i in range(n):
        A = hsv_to_rgb(np.array([(h + step * i) / 360, s / 100, v / 100]))
        ret[i] = A
    return ret


def knn(train_files, data_files, params, limits, n_neighbors=5, colorshift=45):
    train_dataframe = []
    for file in train_files:
        temp = pd.read_csv(f"data\\arrival_annotated\\{file + '.csv'}",
                           dtype={'icao24': str,
                                  'destination': str,
                                  'callsign': str,
                                  'flight_id': str})
        train_dataframe.append(temp[temp["usefull"]])
    train_dataframe = pd.concat(train_dataframe)
    train_dataframe = scaling(train_dataframe, limits, width=2)
    train_data = []
    for p in params:
        train_data.append(train_dataframe[p].to_numpy(dtype=np.float))

    train_data = np.asarray(train_data)
    train_data = np.transpose(train_data)
    neigh = KNeighborsClassifier(n_neighbors=n_neighbors)
    neigh.fit(train_data, train_dataframe["loitering"])
    for file in range(0, len(data_files)):
        print(f"data\\arrival_modified\\{data_files[file].split('_')[0]}\\{data_files[file][:-1]}.csv")
        file_data = pd.read_csv(f"data\\arrival_modified\\{f[file].split('_')[0]}\\{f[file][:-1]}.csv",
                                dtype={'icao24': str,
                                       'destination': str,
                                       'callsign': str,
                                       'flight_id': str})
        temp = scaling(file_data[file_data["usefull"]], limits, width=2)
        temp_data = []
        for p in params:
            temp_data.append(temp[p].to_numpy(dtype=np.float))

        temp_data = np.asarray(temp_data)
        temp_data = np.transpose(temp_data)
        file_data["loitering"] = np.zeros(len(file_data), dtype=int)
        file_data.loc[file_data["usefull"], "loitering"] = neigh.predict(temp_data)
        file_data.to_csv(f'data\\arrival_annotated\\{data_files[file][:-1]}.csv', index=False)
    print("debug")


if __name__ == "__main__":
    train = ["AAL92_20575", "AEE5SZ_4453", "AEA1671_507", "AEA1671_479", "AEA1671_476", "ACA878_20920", "AFL2390_3085",
             "AFL2390_3059", "AFL2390_3120", "AFL2486_3096", "AUA2728_3799"]
    data = []
    f = open("data\\turnaround_2.list", "r").readlines()
    for file in range(0, min(1000, len(f))):
        if f[file] not in train:
            data.append(f[file])

    params = [  # "timestamp", comp ignore
        #"altitude",
        # "callsign", comp ignore
        #"geoaltitude",
        "groundspeed",
        # "icao24", comp ignore
        # "lastseen", comp ignore
        "latitude",
        "longitude",
        # "origin", comp ignore
        #"track",
        #"vertical_rate",
        #"distance",
        # "flight_id", comp ignore
        # "runway",
        #"geo_change",
        "alt_change",
        #"heading_change",
        # "geo_track",
        # "geo_track_change",
        "vel_change",
        #"cumulativ_track",
        # "cumulativ_geo_track",
        # "usefull", comp ignore
        # "loitering" comp ignore
    ]
    limits = pd.read_csv(f"data\\arrival_modified\\limits.csv")
    knn(train, data, params, limits, n_neighbors=25)
