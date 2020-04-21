# stuff we will use
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
import numpy as np
from matplotlib.colors import hsv_to_rgb


# N integers to N distinguishable colors function, Note: works but recommend manually selecting colors if possible
def colors(n, colorshift):
    ret = np.array([0, 0, 0])
    start = colorshift
    h = start
    s = 100
    v = 100
    step = (360 - start) / (n - 1)
    for i in range(n):
        A = hsv_to_rgb(np.array([h / 360, s / 100, v / 100]))
        ret = np.vstack((ret,A))
        h += step
    return ret[1:,:]

def kmeans(data, N,
           ignore_parameters = "none",
           dont_scale_parameters = "none",
           return_centroids = False,
           return_colors_rgb = False,
           colorshift = 90):

    # select desired parameters ["timestamp","callsign","icao24","lastseen","flight_id","origin"]
    if ignore_parameters != "none":
        df = data.drop(ignore_parameters,axis=1)
    else:
        df = data
    if dont_scale_parameters != "none":
        scaled_data = df.drop(dont_scale_parameters,axis=1)
    else:
        scaled_data = df

    # scale and execute kmeans
    scaled_data = pd.DataFrame(scale(scaled_data),columns=scaled_data.columns)
    df[scaled_data.columns] = scaled_data
    km = KMeans(n_clusters=N)
    groups = km.fit_predict(df)
    df["cluster"] = groups

    # execute color function
    if return_colors_rgb:
        C = np.char.array("empty")
        colours = colors(N,colorshift)
        for i in range(0, np.size(df.cluster)):
            if C[0] == "empty":
                C = np.char.array(str(colours[df.cluster[i]]))
            else:
                C = np.vstack((C, str(colours[df.cluster[i]])))
        df["colors"] = C

    # return values
    if not return_centroids:
        return df
    else:
        centroids = km.cluster_centers_
        return df, centroids
