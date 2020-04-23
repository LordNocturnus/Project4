# stuff we will/might use
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb
from mpl_toolkits.mplot3d import Axes3D


# N integers to N distinguishable color_range function, Note: works but recommend manually selecting color_range if possible
def colors(n, colorshift):
    ret = []
    start = colorshift
    h = start
    s = 100
    v = 100
    step = (360 - start) / (n - 1)
    for i in range(n):
        A = hsv_to_rgb(np.array([h / 360, s / 100, v / 100]))
        ret.append(A)
        h += step
    return ret

def Kmeans_single_flight(filelocation,N,list_of_Parameter,plot=True,return_cents=False,return_colors_rgb=False,colorshift=90):

    # initial values & setup
    C = "empty"
    N = N
    file = filelocation
    df = pd.read_csv(file)
    #scaledata = df[["altitude","geoaltitude","groundspeed","latitude","longitude","track","vertical_rate","distance","runway"]]
    scaledata = df[list_of_Parameter]
    df_scale = pd.DataFrame(scale(scaledata),columns=scaledata.columns)

    # Kmeans
    km = KMeans(n_clusters=N)
    groups = km.fit_predict(df_scale[list_of_Parameter])
    df["cluster"] = groups

    # execute color function
    if return_colors_rgb:
        colours = colors(N,colorshift)
        for i in range(0, np.size(df.cluster)):
            if C == "empty":
                C = np.array(list(colours[df.cluster[i]]))
            else:
                C = np.vstack((C, list(colours[df.cluster[i]])))

        C_string = []
        for i in C:
            C_string.append(str(i))
        df["color_range"] = C_string

    # plot
    if plot:
        fig = plt.figure()
        ax = Axes3D(fig)
        if C == "empty":
            colours = colors(N,colorshift)
            for i in range(0,np.size(df.cluster)):
                if C == "empty":
                    C = np.array(list(colours[df.cluster[i]]))
                else:
                    C = np.vstack((C,list(colours[df.cluster[i]])))

        ax.scatter([df.latitude], [df.longitude], [df.altitude], c=C)
        ax.set_xlabel("latitude")
        ax.set_ylabel("longitude")
        ax.set_zlabel("altitude")
        plt.show()

    # return values
    if not return_cents:
        return df
    else:
        centroids = km.cluster_centers_
        return df, centroids
