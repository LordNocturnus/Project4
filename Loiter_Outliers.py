import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.display import display
import matplotlib.dates as md #needed to convert time
import os
from matplotlib.colors import hsv_to_rgb
from matplotlib.patches import Polygon
import math

def filterpoints(data, clustersize = 10):

    filtered = data.copy(deep=True)

    for i in range(math.floor(len(data["loitering"])/clustersize)):    
        rows = data.iloc[0+clustersize*i:clustersize+clustersize*i]
        av = np.average(rows["loitering"])
        if av < 0.5: 
            filtered.iloc[0+clustersize*i:clustersize+clustersize*i]["loitering"] = 0
        elif av > 0.5:
            filtered.iloc[0+clustersize*i:clustersize+clustersize*i]["loitering"] = 1
    return filtered

def plotloiter(data):
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    timestamps = md.date2num(data["timestamp"])
    plt.figure(figsize=(10,4))
    plt.title("Loiter")
    plt.xticks( rotation=25 )
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.scatter(timestamps, data["loitering"], alpha = 1, marker = ".")
    plt.show()

flight_num = 2
cluster_size = 30

annot_list = os.listdir(os.getcwd() + '/data/arrival_annotated')

if 'arrival_annot_filtered' not in os.listdir(os.getcwd() + '/data'):
    os.mkdir(os.getcwd() + f"/data/arrival_annot_filtered")

for f in range(0, min(len(annot_list), flight_num)):
    file = annot_list[f]
    if file[-4:] == ".csv":
        print(file)
        data = pd.read_csv(f"data/arrival_annotated/{file}")
        filtereddata = filterpoints(data, clustersize = cluster_size)   
        #for comparison:
        #plotloiter(data)
        #plotloiter(filtereddata)
        filtereddata.to_csv(f'data/arrival_annot_filtered/{file}', index=False)

