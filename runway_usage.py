import pandas as pd
from datetime import datetime
from textwrap import wrap
import matplotlib
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt

from IPython.core.display import display


# data paths:
path_runway10_28 = "data/runway10_28.csv"
path_runway14_32 = "data/runway14_32.csv"
path_runway16_34 = "data/runway16_34.csv"


# import runway data
runway10_28 = pd.read_csv(path_runway10_28)
runway14_32 = pd.read_csv(path_runway14_32)
runway16_34 = pd.read_csv(path_runway16_34)

# create single dataframe
df = pd.concat([runway10_28, runway14_32, runway16_34], ignore_index=True)
df["timestamp"] = pd.to_datetime(df["timestamp"])



#______________________________________________________________________________________________________________________




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
            concept = 'East'
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
            concept = 'East'
        elif hour == 1:
            concept = 'East'
        else:
            concept = None

    return concept




# resampling by hour, grouping by runway/movement type
arrivals_hourly = df[df['arriving'] == True].set_index("timestamp").groupby([pd.Grouper(freq='H'), 'runway']).size()
departures_hourly = df[df['arriving'] == False].set_index("timestamp").groupby([pd.Grouper(freq='H'), 'runway']).size()
runway_hourly = arrivals_hourly.to_frame().merge(departures_hourly.to_frame(), how='outer', left_index=True, right_index=True)
runway_hourly.columns = ['arrivals', 'departures']
runway_hourly = runway_hourly.fillna(0).astype(int)

max_hourly = runway_hourly.groupby([runway_hourly.index.get_level_values('timestamp').hour, 'runway' ]).max()
mean_hourly = runway_hourly.groupby([runway_hourly.index.get_level_values('timestamp').hour, 'runway' ]).mean()



# grouping by hour
flights_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='H')]).size()

flights_hourly = flights_hourly.reset_index()
flights_hourly.columns = ['timestamp', 'count']
flights_hourly['hour'] = flights_hourly['timestamp'].dt.hour
flights_hourly['dayname'] = flights_hourly['timestamp'].dt.day_name()
flights_hourly['concept'] = flights_hourly.apply(concept_sorter,axis=1)

# print(flights_hourly)













#stat analysis by concepts
mean_concepts = flights_hourly.groupby('concept')['count'].mean()
sum_concepts = flights_hourly.groupby('concept')['count'].sum()
# sum_concepts = sum_concepts.reset_index()
# sum_concepts['percent'] = sum_concepts['count'].apply(lambda x: x/38987)
# print(sum_concepts)



#________________________________________________________________________________________________________________________
#plotting stuff

plt.figure(1, figsize=(35,8))
plt.title("Total Flight Movements per Hour")

for cp in flights_hourly.concept.unique():
    conc_ = flights_hourly[flights_hourly['concept']==cp][['timestamp', 'count']]
    conc_ = conc_[conc_['count']> 20]
    print(conc_)

    plt.scatter(conc_['timestamp'].values, conc_['count'].values, label=cp)
plt.axhline(y=50, xmin=0.0, xmax=1.0, color='r')
plt.legend()
axes = plt.gca()
axes.set_ylim([20,65])








# plt.figure(2)
# mean_plot = mean_concepts.plot.bar(
#     x='concept',
#     y='count',
#     rot=0,
#     title="Mean Hourly Flight Movements by Concept"
# )

# sum_plot = sum_concepts.plot.pie(
#     x='concept',
#     y='count',
#     rot=0,
#     title="Total Flight Movements by Concept"
# )

def mpl_active_bounds(ax):
    def on_xlims_change(event_ax):
        
        limits =  "new x-axis limits: "+'"'+ matplotlib.dates.num2date(event_ax.get_xlim()[0]).strftime("%Y-%m-%d %H:%M:%S+00:00")+'","'+matplotlib.dates.num2date(event_ax.get_xlim()[1]).strftime("%Y-%m-%d %H:%M:%S+00:00")+'"'
        print(limits)
    ax.callbacks.connect("xlim_changed", on_xlims_change)

def part_of_total_flights(start_date, end_date, subplotnum, truncatenum, percentile):

    cleaned_flights_hourly = flights_hourly
    cleaned_flights_hourly = cleaned_flights_hourly[cleaned_flights_hourly['count']> truncatenum]
    cleaned_flights_hourly = cleaned_flights_hourly.loc[cleaned_flights_hourly['timestamp'].between(start_date,end_date, inclusive=True)]

    lineheight = cleaned_flights_hourly['count'].quantile(percentile/100)

    yticks = np.arange(0, 70, 5)
    yticks = np.insert(yticks, 1, lineheight, 0)
    yticks = np.sort(yticks)

    ax = plt.subplot(subplotnum)

    limit_cleaned_flights_hourly = cleaned_flights_hourly[cleaned_flights_hourly['count'] > lineheight]
    rednum = limit_cleaned_flights_hourly['count'].size

    xfmt = matplotlib.dates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.xaxis.set_major_formatter(xfmt)
    ax.plot(cleaned_flights_hourly['timestamp'].values, cleaned_flights_hourly['count'].values)
    title = ax.set_title("\n".join(wrap(f"Total Flight Movements per Hour (truncated above {truncatenum})", 50)))
    title.set_y(1.05)
    ax.axhline(y=lineheight, xmin=0.0, xmax=1.0, color='r', label="{}th percentile; n={}".format(percentile, rednum))
    ax.set_yticks(yticks)
    ax.grid('on', which='minor', axis='y', linestyle=':', linewidth=0.5)
    ax.legend()
    axes = plt.gca()
    axes.set_ylim([truncatenum,63])

    ax.scatter(limit_cleaned_flights_hourly['timestamp'].values, limit_cleaned_flights_hourly['count'].values,
               color='red')
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    mpl_active_bounds(ax)

 #max_hourly.unstack().plot(kind="bar", stacked=True)
 #plt.title("Maximum Flight Movements per Runway by Hour")
 #ax = plt.gca()
 #ytick = np.arange(0,150,5)
 #ax.set_yticks(ytick, minor=True)
 #ax.grid('off', which='major', axis='y', linestyle='--', linewidth=0.5)
 #ax.grid('on', which='minor', axis='y', linestyle=':', linewidth=0.5)



#mean_hourly.unstack().plot(kind="bar", rot=0, stacked=True)
#plt.title("Mean Flight Movements per Runway by Hour")
#ax = plt.gca()
#ytick = np.arange(0,75,5)
#ax.set_yticks(ytick, minor=True)
#ax.grid('off', which='major', axis='y', linestyle='--', linewidth=0.5)
#ax.grid('on', which='minor', axis='y', linestyle=':', linewidth=0.5)

#part_of_total_flights('2019-10-01', "2019-11-30", 111, 30, 55)
#plt.show()






