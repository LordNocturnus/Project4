import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import sys
import os

parking_data = pd.read_csv(os.path.join(os.getcwd()+"\\data\\howmanyairplanes2.csv"))

def plot_aircraft_parking(dataframe):
    dates = dataframe["timestamp"]
    if type(pd.array(dataframe["timestamp"])[0]) == str:
        #Convert dates list into datetime objects if not already
        dates = [datetime.strptime(date,"%Y-%m-%d %H:%M:%S+00:00") for date in dates]
    
    plt.figure(figsize = (16,9))
    timestamps = matplotlib.dates.date2num(dates)
    plt.xticks( rotation=25 )
    ax=plt.gca()
    xfmt = matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(timestamps, dataframe["amount"] ,color = 'black',linewidth = 1)

    #plt.savefig("aircraft_parked.pdf",bbox= 'tight')
    plt.show()

def part_of_aircraft_parking(start,end):
    start_date = datetime.strptime(start,"%Y-%m-%d %H:%M:%S+00:00")
    end_date = datetime.strptime(end,"%Y-%m-%d %H:%M:%S+00:00")
    parking_data["timestamp"] = [datetime.strptime(date,"%Y-%m-%d %H:%M:%S+00:00") for date in pd.array(parking_data["timestamp"])]
    condition = (parking_data["timestamp"]>= start_date) & (parking_data["timestamp"] <= end_date)
    part_of_dataframe = parking_data[condition]
    plot_aircraft_parking(part_of_dataframe)

plot_aircraft_parking(parking_data)
part_of_aircraft_parking("2019-11-14 01:00:00+00:00","2019-11-15 01:00:00+00:00")
