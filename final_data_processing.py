import pandas as pd
from datetime import datetime
from textwrap import wrap
import matplotlib as mpl
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt


def data_processor(start_date, end_date, percentile):


    # data importing

    df = pd.read_csv("data/concept_analysis/concept_analysis.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    concept_devs = pd.read_csv("data/concept_analysis/concept_failures.csv")
    go_arounds = pd.read_csv("data/Go_arounds.csv")



    # getting rid of old runway data, cleaning up names and stuff

    df = df.rename({'new_runway': 'runway'}, axis=1)
    df = df.drop('initial_runway', 1)
    df = df.drop('icao24', 1)
    df = df.drop('flight_id', 1)
    df[['runway', 'scheduled_concept', 'current_concept']] = df[['runway', 'scheduled_concept', 'current_concept']].astype(int)
    df['current_concept'] = df['current_concept'].replace({0: 'North', 1: 'East', 2: 'South', 99: 'Unscheduled'})
    df['scheduled_concept'] = df['scheduled_concept'].replace({0: 'North', 1: 'East', 2: 'South', 99: 'Unscheduled'})


    # resampling by hour, grouping by concept/movement type

    arrivals_hourly = df[df['arriving'] == True].set_index("timestamp").groupby([pd.Grouper(freq='H'), 'current_concept']).size()
    departures_hourly = df[df['arriving'] == False].set_index("timestamp").groupby([pd.Grouper(freq='H'), 'current_concept']).size()
    concept_hourly = arrivals_hourly.to_frame().merge(departures_hourly.to_frame(), how='outer', left_index=True, right_index=True)
    concept_hourly.columns = ['arrivals', 'departures']
    concept_hourly = concept_hourly.fillna(0).astype(int)


    # grouping by hour

    flights_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='H')]).size()
    flights_hourly = flights_hourly.reset_index()
    flights_hourly.columns = ['timestamp', 'count']
    flights_hourly['hour'] = flights_hourly['timestamp'].dt.hour



    # sort hourly flights

    percentile = percentile/100
    cutoff = flights_hourly['count'].quantile(percentile)
    sorted_flights_hourly = flights_hourly[flights_hourly['count'] > cutoff].drop('hour', 1)
    sorted_flights_hourly.columns = ['timestamp', 'fl_mov']

    print(sorted_flights_hourly)

    # sort concept deviations
    concept_devs['timestamp'] = pd.to_datetime(concept_devs['timestamp'])
    concept_devs = concept_devs.drop(["next_concept", "flight_id", "icao24", "match", 'current_concept', 'runway'], 1)
    concept_devs = concept_devs.rename({'new_runway': 'runway'}, axis=1)
    concept_devs[['runway', 'concept']] = concept_devs[['runway', 'concept']].astype(int)
    concept_devs['concept'] = concept_devs['concept'].replace({0: 'North', 1: 'East', 2: 'South', 99: 'Unscheduled', 12: 'East-South'})
    concept_devs = concept_devs.set_index("timestamp").groupby([pd.Grouper(freq='H')]).size()
    concept_devs = concept_devs[concept_devs != 0].reset_index()
    concept_devs.columns = ['timestamp', 'con_dev']


    # print(concept_devs)

    # go_around sorting
    go_arounds['timestamp'] = pd.to_datetime(go_arounds['timestamp'])
    go_arounds = go_arounds.set_index("timestamp").groupby([pd.Grouper(freq='H'), 'flight_id']).size()
    go_arounds = go_arounds[go_arounds != 0].reset_index()
    go_arounds.columns = ['timestamp', 'flight_id', 'go_ar']
    go_arounds = go_arounds.groupby('timestamp').size().reset_index()

    # print(go_arounds)

    sorted_flights_hourly = sorted_flights_hourly.merge(concept_devs, how='outer', on='timestamp')
    go_arounds = go_arounds.merge(sorted_flights_hourly, how='outer', on='timestamp')
    final = go_arounds.set_index('timestamp').fillna(0).astype(int)

    final.columns = ['go_ar', 'fl_mov', 'con_dev',]
    final['fl_mov_norm'] = final['fl_mov'] / cutoff
    final['total'] = final['fl_mov_norm']+final['con_dev']+final['go_ar']
    final = final.drop('fl_mov', 1).reset_index()
    # final = final[final['total'] > 0]

    print(final)
    final.plot.scatter(x='timestamp', y='total', c='total', s=25, cmap=mpl.cm.plasma)
    plt.title("Total Hourly Capacity Markers, {}th percentile".format(percentile))

    ax = plt.gca()
    ytick = np.arange(0,10,1)
    ax.set_yticks(ytick, minor=True)
    ax.grid('on', which='minor', axis='y', linestyle=':', linewidth=0.5)
    ax.grid('on', which='major', axis='y', linestyle='--', linewidth=0.5)
    plt.show()

data_processor("2019-10-01","2019-11-30",50)