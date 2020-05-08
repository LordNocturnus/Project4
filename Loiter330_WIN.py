# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.display import display
import matplotlib.dates as md #needed to convert time
import os

# Useful function to plot all kinds of graphs
def plot_traject(data, traj = True, track = False, cumul_track = True, plot_alt = False, plot_track_change = False, start_at_zero = False):
    
    #convert to correct imestamp format (which is different for the csv's than for the parquet files for some reason)
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    
    if traj:
        plt.title("Coordinates of flight")
        plt.axis('equal')
        plt.scatter(data['longitude'], data['latitude'], marker='.',color='b',linewidths=0.01)
    
        # estimates of runways #THESE RUNWAY COORDINATES ARE WRONG AND NEED TO BE CORRECTED!!! (was just example)
        #plt.plot([8.3, 8.45], [47.6, 47.47], color='g')
        #plt.plot([8.5, 8.65], [47.6, 47.47], color='g')

        #plt.plot([8.65, 8.7], [47.2, 46.8], color='y')
        #plt.plot([8.8, 8.85], [47.2, 46.8], color='y')

        plt.show()
    
    
    #convert time
    timestamps = md.date2num(data["timestamp"])
    
    if plot_alt:
        # plots altitude over time
        plt.figure(figsize=(10,4))
        plt.title("Altitude")
        plt.xticks( rotation=25 )
        ax=plt.gca()
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(timestamps, data['geoaltitude'])
        plt.show()
    
    # plot track
    if track:
        plt.figure(figsize=(10,4))
        plt.xticks( rotation=25 )
        ax=plt.gca()
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(timestamps, data['track'])
        plt.title("Track values")
        plt.show()
    
    if cumul_track:
        # plots the cumulative track, i.e. it doesn't jump back down to 0 deg when it crosses 360 deg and forms one continuous graph (see examples)
        kf = data["track"].to_numpy()
        k = 0
        #print(kf)
        for i in range(2,len(kf)):
            if kf[i-1] > 330+360*k and kf[i] < 30+360*k:
                kf[i:] += 360
                k += 1
            elif kf[i-1] < 30 + 360*k and kf[i] > 330 + 360*k:
                kf[i:] -= 360
                k -= 1  
        if start_at_zero:
            kf = kf-kf[0]
        plt.figure(figsize=(10,4))
        plt.title("Cumulative track")
        plt.plot(timestamps,kf)
        #plt.set_xticklabels([])
        plt.show()
        #print(kf)
        
    if plot_track_change:
        # changes in track (current minus last value) # Might need to adjust for outliers as the graph now looks flat
        plt.figure(figsize=(10,4))
        plt.title("Track changes")
        track_changes = data['track'].values[1:]-data['track'].values[:-1]
        #track_changes = data["geo_track_change"]
        plt.xticks( rotation=25 )
        ax=plt.gca()
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(timestamps[1:], track_changes)
        plt.show()

# testing:
#ddd = pd.read_csv(".\\data\\arrival_modified\\2KYCM\\2KYCM_3248.csv")
#plot_traject(ddd, traj = True, track = True, cumul_track = True, plot_alt = True, plot_track_change = True, start_at_zero = False)


# Find failed landings '''
def calc_cumul_track(data, plot_cumul = False, plot_others = True):
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    
    timestamps = md.date2num(data["timestamp"])
    
    go_around = False
    unclear = False
    
    kf = data["track"].to_numpy()
    k = 0
    #print(kf)
    for i in range(1,len(kf)):
        if kf[i-1] > 330+360*k and kf[i] < 30+360*k:
            kf[i:] += 360
            k += 1
        elif kf[i-1] < 30 + 360*k and kf[i] > 330 + 360*k:
            kf[i:] -= 360
            k -= 1
    
    kf = kf-kf[0]   # to start at zero
    
    #print(kf)
    if np.amax(kf) - np.amin(kf) > 330:
        
        go_around = True
        
        if plot_cumul:
            plt.figure(figsize=(10,4))
            plt.title("Cumulative Track")
            plt.xticks( rotation=25 )
            ax=plt.gca()
            xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
            ax.xaxis.set_major_formatter(xfmt)
            plt.plot(timestamps, kf)
            plt.show()
            
        #if you wish to plot:
        if plot_others:
            plot_traject(data, traj = True, track = False, cumul_track = False, plot_alt = False, plot_track_change = False)
    
    if 300 < np.amax(kf) - np.amin(kf) < 330:
        unclear = True
    return go_around, unclear

# Finding loitering flights and returning list:

flight_num = 10000

arrival_list = os.listdir(os.getcwd() + '\\data\\arrival_flights')
#print(arrival_list)

loiterlist = []
unclearlist = []

for f in range(0, min(len(arrival_list), flight_num)):
    if not arrival_list[f].startswith('.') and not arrival_list[f][-4:] == ".csv":
        #print("\nfolder: ", arrival_list[f])
        for file in os.listdir(os.getcwd() + f'\\data\\arrival_flights\\{arrival_list[f]}'):
            if file[-4:] == ".csv":
                #print(file)
                data = pd.read_csv(f"data\\arrival_flights\\{arrival_list[f]}\\{file}")
                go_around, unclear = calc_cumul_track(data, plot_cumul = False, plot_others = False)
                if go_around:
                    loiterlist.append(file)
                    #print(file, " is loitering.")
                if unclear:
                    unclearlist.append(file)
                
print(loiterlist)
#print(unclearlist)



