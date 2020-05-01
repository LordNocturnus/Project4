import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import sys
import os

parking_data = pd.read_csv(os.path.join(os.getcwd() + "\\data\\howmanyairplanes2.csv"))


def mpl_active_bounds(ax):
    def on_xlims_change(event_ax):
        
        limits =  "new x-axis limits: "+'"'+ matplotlib.dates.num2date(event_ax.get_xlim()[0]).strftime("%Y-%m-%d %H:%M:%S+00:00")+'","'+matplotlib.dates.num2date(event_ax.get_xlim()[1]).strftime("%Y-%m-%d %H:%M:%S+00:00")+'"'
        print(limits)
    ax.callbacks.connect("xlim_changed", on_xlims_change)


def plot_aircraft_parking(dataframe, subplot_number):
    dates = dataframe["timestamp"]
    if type(pd.array(dataframe["timestamp"])[0]) == str:
        # Convert dates list into datetime objects if not already
        dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00") for date in dates]
    # timestamps = matplotlib.dates.date2num(dates)
    ax = plt.subplot(subplot_number)
    plt.plot(dates, dataframe["amount"], color="black", linewidth=1)
    xfmt = matplotlib.dates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.xaxis.set_major_formatter(xfmt)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    # plt.savefig("aircraft_parked.pdf",bbox= 'tight')
    mpl_active_bounds(ax)


def part_of_aircraft_parking(start, end, subplot_number):
    start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S+00:00")
    end_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S+00:00")
    parking_data["timestamp"] = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S+00:00")for date in pd.array(parking_data["timestamp"])]
    condition = (parking_data["timestamp"] >= start_date) & (parking_data["timestamp"] <= end_date)
    part_of_dataframe = parking_data[condition]
    plot_aircraft_parking(part_of_dataframe, subplot_number)


# plot_aircraft_parking(parking_data,111)
#part_of_aircraft_parking("2019-11-14 01:00:00+00:00", "2019-11-15 01:00:00+00:00", 111)
#plt.show()
