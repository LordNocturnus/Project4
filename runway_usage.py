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


# print(pd.unique(runway_daily['runway']))

def concept_sorter(row):
    weekday = row.index.dayofweek
    hour = row.index.hour
    weekend_days = [5,6]
    week_days = [0,1,2,3,4]

    if weekday in weekend_days:
        if hour in [6, 7, 8]:
            concept = 'South'
        elif hour in [20, 21, 22, 23]:
            concept = 'East'
        elif hour in range(9, 20):
            concept = 'North'
        else:
            concept = None
    elif weekday in week_days:
        if hour == 6:
            concept = 'South'
        elif hour in [21, 22, 23]:
            concept = 'East'
        elif hour in range(7, 21):
            concept = 'North'
        else:
            concept = None
    else:
        concept = None

    return concept

# grouping by hour and runway
runway_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='H'), 'runway']).size() #grouper(freq="H") groups per hour
flights_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='H')]).size()

# flights_hourly = flights_hourly[flights_hourly.index.hour == 6]

flights_hourly = flights_hourly.apply(concept_sorter,axis=1)






# runway_hourly = runway_hourly.reset_index()
# runway_hourly.columns = ['hour', 'runway', 'count']
# print(runway_hourly.index.get_level_values('timestamp'))

#
# for rw in [14, 16, 28, 34, 10, 32]:
#     runway_ = runway_hourly[runway_hourly["runway"] == rw][["hour", "count"]]
#     print(runway_)

# runway_hourly = df.set_index("timestamp")
# runway_hourly = runway_hourly[runway_hourly['arriving'] == False]
# runway_hourly = runway_hourly[runway_hourly['runway'] == 28]
# runway_hourly = runway_hourly.groupby(runway_hourly.index.hour).size()

# create concept hourly dataframes

# # Is weekend function?
def is_weekend(df):
    for num in [0,1,2,3,4]:
        if any(df.index.get_level_values('timestamp').dayofweek == num):
            return False
        else:
            return True


# South Concept Dataframe
scd_wdh = runway_hourly[runway_hourly.index.get_level_values('timestamp').hour == 6]
scd_wdh = scd_wdh[~(scd_wdh.index.get_level_values('timestamp').dayofweek == (5 | 6))]
# scd_wdh = scd_wdh.reset_index()

# scd_weh = runway_hourly[runway_hourly.index.get_level_values('timestamp').hour == (6 | 7 | 8)]
# scd_weh = scd_weh[(scd_wdh.index.get_level_values('timestamp').dayofweek == (5 | 6))]
# scd_weh = scd_weh.reset_index()

# south_concept = pd.concat([scd_wdh, scd_weh])


# East Concept Dataframe
# ecd_wdh = runway_hourly[runway_hourly.index.get_level_values('timestamp').hour == (21 | 22 | 23 )]
# ecd_wdh = ecd_wdh[~(ecd_wdh.index.get_level_values('timestamp').dayofweek == (5 | 6))]

# ecd_weh = runway_hourly[runway_hourly.index.get_level_values('timestamp').hour == (20 | 21 | 22 | 23)]
# ecd_weh = ecd_weh[(ecd_wdh.index.get_level_values('timestamp').dayofweek == (5 | 6))]

# east_concept = pd.concat([ecd_wdh, ecd_weh])

# # North Concept Dataframe
# ncd_wdh = runway_hourly[runway_hourly.index.get_level_values('timestamp').hour == ( 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20)]
# ncd_wdh = ncd_wdh[~(ncd_wdh.index.get_level_values('timestamp').dayofweek == (5 | 6))]
#
# ncd_weh = runway_hourly[runway_hourly.index.get_level_values('timestamp').hour == (9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19)]
# ncd_weh = ncd_weh[(ncd_wdh.index.get_level_values('timestamp').dayofweek == (5 | 6))]
#
# north_concept = pd.concat([ncd_wdh, ncd_weh])

# in_concept = pd.concat([south_concept, north_concept, east_concept])
# print(in_concept)


# plotting stuff
fig, ax = plt.subplots(figsize=(28, 8))
# plt.figure(figsize=(28,8))
ax.set_title("flights per runway per hour")

# for rw in [14, 16, 28, 34]:
#     runway_ = runway_daily[runway_daily['runway']==rw][['day', 'count']]
#     plt.plot(runway_['day'].values, runway_['count'].values, label=rw)

# for rw in [14]:
#     runway_ = runway_hourly[runway_hourly['runway']==rw][['hour', 'count']]
#     print(runway_)
#     plt.plot(runway_['hour'].values, runway_['count'].values, label=rw)
#
# plt.legend()
# plt.show()


# df[(start_date <= df.index.to_pydatetime()) & (end_date >= df.index.to_pydatetime())].plot(grid=True)

# plt.show()
