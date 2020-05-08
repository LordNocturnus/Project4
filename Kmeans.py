# stuff we will use
import os
import pandas as pd
import numpy as np
from copy import deepcopy
from sklearn.cluster import KMeans, DBSCAN
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


def kmeans(data, N, parameters, dont_scale_parameters=None, return_centroids=False, return_colors_rgb=False,
           colorshift=45, plot=False):
    # select desired parameters
    C = "empty"
    df = deepcopy(data)
    for c in data.columns:
        if c not in parameters:
            df = df.drop(c, axis=1)
    if dont_scale_parameters is not None:
        scaled_data = df.drop(dont_scale_parameters, axis=1)
    else:
        scaled_data = df

    # scale and execute kmeans
    scaled_data = scaling(scaled_data, limits, width=1)
    df[scaled_data.columns] = scaled_data
    """km = KMeans(n_clusters=N)
    groups = km.fit_predict(df)
    data["cluster"] = groups"""

    DB = DBSCAN(eps=0.125)
    groups = DB.fit_predict(df)
    data["cluster"] = groups

    # execute color function
    if return_colors_rgb:
        C = np.char.array("empty")
        colors = color_range(len(set(data.cluster)), colorshift)
        for i in range(0, np.size(data.cluster)):
            if C[0] == "empty":
                C = np.char.array(str(colors[data.cluster[i]]))
            else:
                C = np.vstack((C, str(colors[data.cluster[i]])))
        data["color_range"] = C

    if plot:
        # fig = plt.figure(1)
        # ax = Axes3D(fig)
        colors = color_range(len(set(data.cluster)), colorshift)
        C = colors[data.cluster]
        '''if C == "empty":
            
            for i in range(0, np.size(data.cluster)):
                if C == "empty":
                    C = np.array(list(colors[data.cluster[i]]))
                else:
                    C = np.vstack((C, list(colors[data.cluster[i]])))'''

        # ax.scatter([data.latitude], [data.longitude], [data.altitude], c=C)
        # ax.set_xlabel("latitude")
        # ax.set_ylabel("longitude")
        # ax.set_zlabel("altitude")
        fig, axs = plt.subplots(len(df.columns), len(df.columns))
        for c1 in range(0, len(df.columns)):
            for c2 in range(0, len(df.columns)):
                axs[c1, c2].scatter(df[df.columns[c2]], df[df.columns[c1]], c=C)
                axs[c1, c2].set(xlabel=df.columns[c2], ylabel=df.columns[c1])

        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()
        plt.figure(2)
        C = colors[data[data["flight_id"] == data["flight_id"][0]].cluster]
        '''C = "empty"
        if C == "empty":
            colors = color_range(N, colorshift)
            for i in range(0, np.size(data[data["flight_id"] == data["flight_id"][0]].cluster)):
                if C == "empty":
                    C = np.array(list(colors[data[data["flight_id"] == data["flight_id"][0]].cluster[i]]))
                else:
                    C = np.vstack((C, list(colors[data[data["flight_id"] == data["flight_id"][0]].cluster[i]])))'''
        plt.scatter(data[data["flight_id"] == data["flight_id"][0]].latitude,
                    data[data["flight_id"] == data["flight_id"][0]].longitude, c=C)
        plt.show()

    # return values
    if not return_centroids:
        return data, df
    else:
        centroids = km.cluster_centers_
        return data, centroids


if __name__ == "__main__":
    data = []
    flight_lim = 10
    limits = pd.read_csv(f"data\\arrival_modified\\limits.csv")
    folders = os.listdir(os.getcwd() + '\\data\\arrival_modified')
    for f in range(0, min(len(folders), flight_lim)):
        if os.path.isdir(os.getcwd() + f'\\data\\arrival_modified\\{folders[f]}'):
            for file in os.listdir(os.getcwd() + f'\\data\\arrival_modified\\{folders[f]}'):
                print(f"data\\arrival_flights\\{folders[f]}\\{file}")
                temp = pd.read_csv(f"data\\arrival_modified\\{folders[f]}\\{file}", dtype={'icao24': str,
                                                                                           'destination': str,
                                                                                           'callsign': str,
                                                                                           'flight_id': str})
                temp = temp.drop(index=range(0, 2))
                data.append(temp[temp["usefull"]])
    data = pd.concat(data)
    data.index = range(0, len(data.index))
    data, df = kmeans(data, 3, [#"timestamp",
                                                  #"altitude",
                                                  #"geoaltitude",
                                                  #"groundspeed",
                                                  #"lastseen",
                                                  #"track",
                                                  #"vertical_rate",
                                                  #"distance",
                                                  #"runway",
                                                  #"geo_track",
                                                  "latitude",
                                                  "longitude",
                                                  "geo_change",
                                                  "geo_track_change",
                                                  "vel_change",
                                                  ],
                      return_centroids=False, colorshift=90, plot=True)
    # raise NotImplementedError
