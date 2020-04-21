import pandas as pd
from datetime import datetime
import matplotlib
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyModeS
import pyarrow
from IPython.core.display import display


# data paths:
path_runway10_28 = "data/runwaystuff/runway10_28.csv"
path_runway14_32 = "data/runwaystuff/runway14_32.csv"
path_runway16_34 = "data/runwaystuff/runway16_34.csv"


# import runway data
runway10_28 = pd.read_csv(path_runway10_28)
runway14_32 = pd.read_csv(path_runway14_32)
runway16_34 = pd.read_csv(path_runway16_34)

# create single dataframe
df = pd.concat([runway10_28, runway14_32, runway16_34], ignore_index=True)
df["timestamp"] = pd.to_datetime(df["timestamp"])


# date stuff
start_date = datetime(2019, 10, 1)
end_date = datetime(2019, 11, 30)

# grouping by day and runway
runway_daily = (
    df.set_index("timestamp").groupby([pd.Grouper(freq="D"), "runway"]).size()
)  # grouper(freq="D") groups per day
runway_daily = runway_daily.reset_index()
runway_daily.columns = ["day", "runway", "count"]
for rw in [14, 16, 28, 34, 10, 32]:
    runway_ = runway_daily[runway_daily["runway"] == rw][["day", "count"]]



def concept_sorter(row):
    weekday = row['dayname']
    hour = row['hour']

    if weekday in ['Saturday', 'Sunday']:
        if hour in [6, 7, 8]:
            concept = 'South'
        elif hour in [20, 21, 22, 23]:
            concept = 'East'
        elif hour in range(9, 20):
            concept = 'North'
        elif hour in [4,5]:
            concept = 'Early'
        elif hour == 1:
            concept = 'East'
        else:
            concept = None
    else:
        if hour == 6:
            concept = 'South'
        elif hour in [21, 22, 23]:
            concept = 'East'
        elif hour in range(7, 21):
            concept = 'North'
        elif hour in [4,5]:
            concept = 'Early'
        elif hour == 1:
            concept = 'East'
        else:
            concept = None

    return concept

# grouping by hour and runway
runway_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='H'), 'runway']).size() #grouper(freq="H") groups per hour


# grouping by hour
flights_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='H')]).size()

flights_hourly = flights_hourly.reset_index()
flights_hourly.columns = ['timestamp', 'count']
flights_hourly['hour'] = flights_hourly['timestamp'].dt.hour
flights_hourly['dayname'] = flights_hourly['timestamp'].dt.day_name()
flights_hourly['concept'] = flights_hourly.apply(concept_sorter,axis=1)


#stat analysis by concepts
mean_concepts = flights_hourly.groupby('concept')['count'].mean()
sum_concepts = flights_hourly.groupby('concept')['count'].sum()
# sum_concepts = sum_concepts.reset_index()
# sum_concepts['percent'] = sum_concepts['count'].apply(lambda x: x/38987)
# print(sum_concepts)
#plotting stuff


mean_plot = mean_concepts.plot.bar(
    x='concept',
    y='count',
    rot=0,
    title="Mean Hourly Flight Movements by Concept"
)

sum_plot = sum_concepts.plot.pie(
    x='concept',
    y='count',
    rot=0,
    title="Total Flight Movements by Concept"
)


plt.show()






