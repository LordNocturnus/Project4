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


#data paths:
path_runway10_28 = 'data/runwaystuff/runway10_28.csv'
path_runway14_32 = 'data/runwaystuff/runway14_32.csv'
path_runway16_34 = 'data/runwaystuff/runway16_34.csv'


#import runway data
runway10_28 = pd.read_csv(path_runway10_28)
runway14_32 = pd.read_csv(path_runway14_32)
runway16_34 = pd.read_csv(path_runway16_34)

#create single dataframe
df = pd.concat([runway10_28, runway14_32, runway16_34], ignore_index=True)
df['timestamp'] = pd.to_datetime(df['timestamp'])
# df = df.set_index(['timestamp'])
# del df['timestamp']
# df = df.groupby('arriving')['runway'].nunique()


#date stuff
start_date = datetime(2019, 10, 1)
end_date = datetime(2019, 11, 30)

#grouping by day and runway
runway_daily = df.set_index('timestamp').groupby([pd.Grouper(freq='D'), 'runway']).size() #grouper(freq="D") groups per day
runway_daily = runway_daily.reset_index()
runway_daily.columns = ['day', 'runway', 'count']
for rw in [14, 16, 28, 34]:
    runway_ = runway_daily[runway_daily['runway']==rw][['day', 'count']]

# print(pd.unique(runway_daily['runway']))

#grouping by hour and runway
# runway_hourly = df.set_index('timestamp').groupby([pd.Grouper(freq='H')], 'runway').size() #grouper(freq="H") groups per hour
# runway_hourly = runway_hourly.reset_index()
# runway_hourly.columns = ['hour', 'runway', 'count']
runway_hourly = df.set_index('timestamp')
runway_hourly = runway_hourly[(runway_hourly['arriving'] == True) & ('runway' == 14)]
# runway_hourly = runway_hourly.groupby(runway_hourly.index.hour).size()

print(runway_hourly)

#plotting stuff
fig, ax = plt.subplots(figsize=(28,8))
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