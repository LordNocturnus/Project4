import pandas as pd
from datetime import datetime
from datetime import timedelta
from textwrap import wrap
from scipy import signal
import scipy.optimize
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

parking_data = pd.read_csv(os.path.join(os.getcwd() + "\\data\\howmanyairplanes2.csv"))


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
    b, a = signal.butter(1, 1/2000)
    y = signal.filtfilt(b, a, dataframe["amount"])
    x = y-20
    z = y+20
    ax = plt.subplot(subplot_number)
    plt.plot(dates, dataframe["amount"], color="black", linewidth=1)
    plt.plot(dates,y,color="r",linewidth=2)
    #plt.plot(dates,x,dates,z)
    plt.scatter(minimum_points["timestamp"],minimum_points["amount"], color="r")
    plt.scatter(maximum_points["timestamp"],maximum_points["amount"], color="b")
    xfmt = matplotlib.dates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.xaxis.set_major_formatter(xfmt)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    title = ax.set_title("\n".join(wrap(f"Amount of parked aircraft on ZRH between {start} and {end}", 50)))
    title.set_y(1.05)    
    # plt.savefig("aircraft_parked.pdf",bbox= 'tight')
    mpl_active_bounds(ax)


def part_of_aircraft_parking(start, end, subplot_number):
    start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S+00:00")
    end_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S+00:00")
    parking_data["timestamp"] = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00")for date in pd.array(parking_data["timestamp"])]
    condition = (parking_data["timestamp"] >= start_date) & (parking_data["timestamp"] <= end_date)
    part_of_dataframe = parking_data[condition]
    plot_aircraft_parking(part_of_dataframe, subplot_number,start_date,end_date)

def minimum_data(dataframe,start,end):
    delta = timedelta(hours=72)
    start_node = datetime(2019,10,1,5,0,0)
    end_node = start_node+delta
    minimum_data = pd.DataFrame(columns=["timestamp","amount"])
    while end_node<end:
        interval = (dataframe["timestamp"] >= start_node) & (dataframe["timestamp"] <= end_node)
        interval_data = dataframe[interval]
        minimum_index = list(interval_data["amount"]).index(min(interval_data["amount"]))
        minimum_entry = interval_data.iloc[[minimum_index ], :]
        minimum_data = minimum_data.append(minimum_entry)
        start_node+=delta
        end_node+=delta
    return minimum_data

def maximum_data(dataframe,start,end):
    delta = timedelta(hours=72)
    start_node = datetime(2019,10,1,5,0,0)
    end_node = start_node+delta
    maximum_data = pd.DataFrame(columns=["timestamp","amount"])
    while end_node<end:
        interval = (dataframe["timestamp"] >= start_node) & (dataframe["timestamp"] <= end_node)
        interval_data = dataframe[interval]
        maximum_index = list(interval_data["amount"]).index(max(interval_data["amount"]))
        maximum_entry = interval_data.iloc[[maximum_index ], :]
        maximum_data = maximum_data.append(maximum_entry)
        start_node+=delta
        end_node+=delta
    return maximum_data

plt.figure(figsize=(16,9))
#part_of_aircraft_parking("2019-11-14 01:00:00+00:00", "2019-11-15 01:00:00+00:00", 111)
part_of_aircraft_parking("2019-10-01 04:01:12+00:00","2019-11-30 22:13:46+00:00", 111)
plt.show()
