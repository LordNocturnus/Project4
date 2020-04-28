# stuff we will use
import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from matplotlib.colors import hsv_to_rgb


def scaling(data, limits, width=2):
    for c in limits.columns:
        try:
            data[c] = (data[c] - limits[c][1]) / (limits[c][2] - limits[c][0]) * width
        except:
            pass
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


def kmeans(data, N,
           ignore_parameters=None,
           dont_scale_parameters=None,
           return_centroids=False,
           return_colors_rgb=False,
           colorshift=90,
           scale_function=scale):
    # select desired parameters
    if ignore_parameters is not None:
        df = data.drop(ignore_parameters, axis=1)
    else:
        df = data
    if dont_scale_parameters is not None:
        scaled_data = df.drop(dont_scale_parameters, axis=1)
    else:
        scaled_data = df

    # scale and execute kmeans
    scaled_data = pd.DataFrame(scale_function(scaled_data), columns=scaled_data.columns)
    df[scaled_data.columns] = scaled_data
    km = KMeans(n_clusters=N)
    groups = km.fit_predict(df)
    df["cluster"] = groups

    # execute color function ["timestamp","callsign","icao24","lastseen","flight_id","origin"]
    if return_colors_rgb:
        C = np.char.array("empty")
        colors = color_range(N, colorshift)
        for i in range(0, np.size(df.cluster)):
            if C[0] == "empty":
                C = np.char.array(str(colors[df.cluster[i]]))
            else:
                C = np.vstack((C, str(colors[df.cluster[i]])))
        df["color_range"] = C

    # return values
    if not return_centroids:
        return df
    else:
        centroids = km.cluster_centers_
        return df, centroids


if __name__ == "__main__":
    limits = pd.read_csv(f"data\\arrival_modified\\limits.csv")
    for folder in os.listdir(os.getcwd() + '\\data\\arrival_modified'):
        if os.path.isdir(os.getcwd() + f'\\data\\arrival_modified\\{folder}'):
            for file in os.listdir(os.getcwd() + f'\\data\\arrival_modified\\{folder}'):
                print(f"data\\arrival_flights\\{folder}\\{file}")
                data = pd.read_csv(f"data\\arrival_modified\\{folder}\\{file}", dtype={'icao24': str,
                                                                                       'destination': str,
                                                                                       'callsign': str,
                                                                                       'flight_id': str})
                scaled = scaling(data, limits)
                raise NotImplementedError