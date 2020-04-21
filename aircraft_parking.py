import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import sys
import os

parking_data = pd.read_csv(os.path.join(os.getcwd()+"\\data\\howmanyairplanes2.csv")).values

dates = parking_data[:,0]
#Convert dates list into datetime objects
for i in range(len(dates)): 
    dates[i] = datetime.strptime(dates[i],"%Y-%m-%d %H:%M:%S+00:00")
#Convert to matplotlib numbers
date_values = matplotlib.dates.date2num(dates)

plt.plot(date_values,parking_data[:,1])
plt.show()
