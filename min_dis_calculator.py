from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import itertools
import math
import os


def N(a, b, phi):
    return a ** 2 / np.sqrt(np.square(a * np.cos(phi)) + np.square(b * np.sin(phi)))


earth_radius = 6378.1370
earth_polar = 6356.7523
num = 60 * 60

data_arrival = pq.read_table("data/arrival_dataset.parquet")
data_arrival = data_arrival.to_pandas()
data_departure = pq.read_table("data/departure_dataset.parquet")
data_departure = data_departure.to_pandas()
data_arrival = data_arrival.append(data_departure)
del data_departure
data_arrival["latitude"] = np.radians(data_arrival["latitude"])
data_arrival["longitude"] = np.radians(data_arrival["longitude"])
data_arrival["geoaltitude"] = data_arrival["geoaltitude"] * 0.3048 / 1000
data_arrival["X_ground"] = (N(earth_radius, earth_polar, data_arrival["latitude"]) + 0) * np.cos(
    data_arrival["latitude"]) * np.cos(data_arrival["longitude"])
data_arrival["X_air"] = (N(earth_radius, earth_polar, data_arrival["latitude"]) + data_arrival["geoaltitude"]) * np.cos(
    data_arrival["latitude"]) * np.cos(data_arrival["longitude"])
data_arrival["Y_ground"] = (N(earth_radius, earth_polar, data_arrival["latitude"]) + 0) * np.cos(
    data_arrival["latitude"]) * np.sin(data_arrival["longitude"])
data_arrival["Y_air"] = (N(earth_radius, earth_polar, data_arrival["latitude"]) + data_arrival["geoaltitude"]) * np.cos(
    data_arrival["latitude"]) * np.sin(data_arrival["longitude"])
data_arrival["Z_ground"] = (earth_polar ** 2 / (earth_radius ** 2) * N(earth_radius, earth_polar,
                                                                       data_arrival["latitude"]) + 0) * np.sin(
    data_arrival["latitude"])
data_arrival["Z_air"] = (earth_polar ** 2 / (earth_radius ** 2) * N(earth_radius, earth_polar,
                                                                    data_arrival["latitude"]) + data_arrival[
                             "geoaltitude"]) * np.sin(data_arrival["latitude"])

times = sorted(list(set(data_arrival["timestamp"])))
res = np.full((math.floor(len(times) / num), 3), np.nan, dtype=np.float)


for t in range(0, math.floor(len(times) / num)):
    print(t * num / len(times))
    res[t][0] = datetime.timestamp(times[t * num])
    temp_ground = np.asarray([np.asarray(data_arrival[data_arrival["timestamp"] == times[t * num]]["X_ground"]),
                              np.asarray(data_arrival[data_arrival["timestamp"] == times[t * num]]["Y_ground"]),
                              np.asarray(data_arrival[data_arrival["timestamp"] == times[t * num]]["Z_ground"])])
    temp_air = np.asarray([np.asarray(data_arrival[data_arrival["timestamp"] == times[t * num]]["X_air"]),
                           np.asarray(data_arrival[data_arrival["timestamp"] == times[t * num]]["Y_air"]),
                           np.asarray(data_arrival[data_arrival["timestamp"] == times[t * num]]["Z_air"])])
    temp_ground = temp_ground.transpose()
    if len(temp_ground) > 1:
        temp_air = temp_air.transpose()
        temp_ground = np.asarray([i for i in itertools.permutations(temp_ground, 2)])
        temp_air = np.asarray([i for i in itertools.permutations(temp_air, 2)])

        res[t][1] = np.min(np.sqrt(np.sum(np.square(temp_ground[:, 0] - temp_ground[:, 1]))))
        res[t][2] = np.min(np.sqrt(np.sum(np.square(temp_air[:, 0] - temp_air[:, 1]))))

res = res.transpose()
plt.plot(res[0], res[1])
plt.plot(res[0], res[2])
np.savetxt('data/distances.csv', res, delimiter=',')