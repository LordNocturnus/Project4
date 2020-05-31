import pandas as pd
from datetime import datetime
from datetime import timedelta
from textwrap import wrap
from scipy import signal
from scipy import interpolate
import scipy.optimize
import statistics
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

parking_data = pd.read_csv(os.path.join(os.getcwd() + "\\data\\howmanyairplanes2.csv"))
commercial_data = pd.read_csv(os.path.join(os.getcwd() +  "\\data\\ground_usage_commercial.csv"))
non_commercial_data = pd.read_csv(os.path.join(os.getcwd() +  "\\data\\ground_usage_non_commercial.csv"))

def mpl_active_bounds(ax):
    def on_xlims_change(event_ax):
        
        limits =  "new x-axis limits: "+'"'+ matplotlib.dates.num2date(event_ax.get_xlim()[0]).strftime("%Y-%m-%d %H:%M:%S+00:00")+'","'+matplotlib.dates.num2date(event_ax.get_xlim()[1]).strftime("%Y-%m-%d %H:%M:%S+00:00")+'"'
        print(limits)
    ax.callbacks.connect("xlim_changed", on_xlims_change)


def plot_aircraft_parking(dataframe, subplot_number,start,end):
    dates = dataframe["timestamp"]
    if type(pd.array(dataframe["timestamp"])[0]) == str:
        # Convert dates list into datetime objects if not already
        dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00") for date in dates]
    minimum_points = minimum_data(dataframe,start,end)
    maximum_points = maximum_data(dataframe,start,end)
    mean_points = mean_data(dataframe,start,end)
    #min_max_points = min_max_data(dataframe,start,end)
    x_min,ymin = interpolate_data(minimum_points)
    x_max,y_max = interpolate_data(maximum_points)
    x_mean,y_mean = interpolate_data(mean_points)
    ax = plt.subplot(subplot_number)
    #ax.plot(x_min,ymin,color="r", alpha = 0.5 ,linestyle='--')
    #ax.plot(x_max,y_max,color="b", alpha = 0.5,linestyle='--')
    #ax.plot(min_max_points["timestamp"],min_max_points["amount"],color = 'b')
    #b, a = signal.butter(1, 1/2000)
    #y = signal.filtfilt(b, a, dataframe["amount"]) lowpass signal filter
    ax.plot(dates, dataframe["amount"], color="black", linewidth=0.5)
    #ax.plot(dates,y,color="r",linewidth=2)
    #ax.scatter(minimum_points["timestamp"],minimum_points["amount"], color="r")
    #ax.scatter(maximum_points["timestamp"],maximum_points["amount"], color="b")
    ax.plot(x_mean,y_mean,color="r",linewidth=2)
    xfmt = matplotlib.dates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_formatter(xfmt)
    time_limits = ["2019-10-01 00:00:00","2019-12-01 00:00:00"]
    time_limits = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in time_limits]
    #ax.set_xlim((time_limits)) 
    #ax.set_ylim((140,300))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    #title = ax.set_title("\n".join(wrap(f"Amount of parked aircraft on ZRH between {time_limits[0]} and {time_limits[1]}", 50)),{"size":20})
    #title.set_y(1.05)    
    plt.legend(handles=[matplotlib.lines.Line2D([0], [0], color='r', lw=4, label='Mean',linestyle='-')],                             
        loc="lower right", 
        prop={"size":15})
    #unused legend handles
    #matplotlib.lines.Line2D([0], [0], color='b', alpha = 0.5, lw=2, label='Upper bound',linestyle='--')
    #matplotlib.lines.Line2D([0], [0], color='r', alpha = 0.5, lw=2, label='Lower bound',linestyle='--')]

    ax.grid('off', which='major', axis='y', linestyle='--', linewidth=0.8)
    ax.tick_params(axis='both', which='major', labelsize=13)
    plt.xlabel("Date",{"size":18})
    plt.ylabel("Amount of aircraft parked at ZRH",{"size":18})
    #plt.savefig("aircraft_parked.pdf",bbox_inches= 'tight')
    mpl_active_bounds(ax)
    


def part_of_aircraft_parking(start, end, subplot_number, dataframe):
    dataframe = dataframe.sort_values("timestamp")
    start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S+00:00")
    end_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S+00:00")
    dataframe["timestamp"] = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00") for date in pd.array(dataframe["timestamp"])]
    condition = (dataframe["timestamp"] >= start_date) & (dataframe["timestamp"] <= end_date)
    part_of_dataframe = dataframe[condition]
    plot_aircraft_parking(part_of_dataframe, subplot_number,start_date,end_date)


def minimum_data(dataframe,start,end):
    delta = timedelta(days=2)
    start_node = datetime(2019,10,1,5,0,0)
    end_node = start_node+delta
    minimum_data = pd.DataFrame(columns=["timestamp","amount"])
    while end_node<end:
        interval = (dataframe["timestamp"] >= start_node) & (dataframe["timestamp"] <= end_node)
        interval_data = dataframe[interval]
        if len(interval_data["amount"])!=0:
            minimum_index = list(interval_data["amount"]).index(min(interval_data["amount"]))
            minimum_entry = interval_data.iloc[[minimum_index ], :]
            minimum_data = minimum_data.append(minimum_entry)
        start_node+=delta
        end_node+=delta
    return minimum_data


def maximum_data(dataframe,start,end):
    delta = timedelta(days=3)
    start_node = datetime(2019,10,1,5,0,0)
    end_node = start_node+delta
    maximum_data = pd.DataFrame(columns=["timestamp","amount"])
    while end_node<end:
        interval = (dataframe["timestamp"] >= start_node) & (dataframe["timestamp"] <= end_node)
        interval_data = dataframe[interval]
        if len(interval_data["amount"])!=0:
            maximum_index = list(interval_data["amount"]).index(max(interval_data["amount"]))
            maximum_entry = interval_data.iloc[[maximum_index ], :]
            maximum_data = maximum_data.append(maximum_entry)
        start_node+=delta
        end_node+=delta
    end_entry = pd.DataFrame(np.array([[datetime.strptime("2019-11-30 05:50:21", "%Y-%m-%d %H:%M:%S"),276]]),columns=["timestamp","amount"])
    maximum_data = maximum_data.append(end_entry)
    return maximum_data


def mean_data(dataframe,start,end):
    delta = timedelta(hours=36)
    start_node = datetime(2019,10,1,5,0,0)
    end_node = start_node+delta
    mean_data = pd.DataFrame(columns=["timestamp","amount"])
    while end_node<end:
        interval = (dataframe["timestamp"] >= start_node) & (dataframe["timestamp"] <= end_node)
        interval_data = dataframe[interval]
        if len(interval_data["amount"])!=0:
            mean = statistics.mean(pd.array(interval_data["amount"]))
            mean_entry = pd.DataFrame(np.array([[(end_node-start_node)/2 + start_node, mean ]]),columns=['timestamp', 'amount'])
            mean_data = mean_data.append(mean_entry)
        start_node+=delta
        end_node+=delta
    return mean_data


def min_max_data(dataframe,start,end):
    delta = timedelta(days=1.1)
    start_node = datetime(2019,10,1,5,0,0)
    end_node = start_node+delta
    min_max_data = pd.DataFrame(columns=["timestamp","amount"])
    while end_node<end:
        interval = (dataframe["timestamp"] >= start_node) & (dataframe["timestamp"] <= end_node)
        interval_data = dataframe[interval]
        if len(interval_data["amount"])!=0:
            maximum_index = list(interval_data["amount"]).index(max(interval_data["amount"]))
            maximum_entry = interval_data.iloc[[maximum_index ], :]
            minimum_index = list(interval_data["amount"]).index(min(interval_data["amount"]))
            minimum_entry = interval_data.iloc[[minimum_index ], :]
            min_max = maximum_entry["amount"].values-minimum_entry["amount"].values
            min_max_entry = pd.DataFrame(np.array([[(end_node-start_node)/2 + start_node, min_max ]]),columns=['timestamp', 'amount'])
            min_max_data = min_max_data.append(min_max_entry)
        start_node+=delta
        end_node+=delta
    return min_max_data


def interpolate_data(dataframe):
    dates = dataframe["timestamp"]
    xdata = matplotlib.dates.date2num(dates)
    ydata = np.array(dataframe["amount"])
    a,b = xdata[0],xdata[-1]
    x_out = np.linspace(a,b,38135)
    tck = interpolate.splrep(xdata, ydata, s=0)
    ynew = interpolate.splev(x_out, tck, der=0)
    return x_out,ynew

plt.figure(figsize=(16,9))
#part_of_aircraft_parking("2019-11-14 01:00:00+00:00", "2019-11-15 01:00:00+00:00", 111)
#part_of_aircraft_parking("2019-10-01 04:01:12+00:00","2019-11-30 22:13:46+00:00", 111, parking_data)
part_of_aircraft_parking("2019-10-01 04:01:12+00:00","2019-11-30 22:13:46+00:00", 111, commercial_data)
#part_of_aircraft_parking("2019-10-01 04:01:12+00:00","2019-11-30 22:13:46+00:00", 111, non_commercial_data)
plt.show()
