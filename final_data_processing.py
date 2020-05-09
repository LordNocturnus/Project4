import pandas as pd
from datetime import datetime
from textwrap import wrap
import matplotlib as mpl
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt
import os
import statistics

def data_processor(start_date, end_date, percentile):


    # data importing

    df = pd.read_csv("data/concept_analysis/concept_analysis.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    concept_devs = pd.read_csv("data/concept_analysis/concept_failures.csv")
    go_arounds = pd.read_csv("data/Go_arounds.csv")
    loitering = pd.read_csv("data/loitering.csv")



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


    mean_concepts = concept_hourly.groupby('current_concept')[['arrivals', 'departures']].mean()

        # plotting mean concept flight movements

    ax = mean_concepts.plot(kind="bar", rot=0, stacked=True, color=['b', 'r'])

    plt.title("Mean Hourly Flight Movements per Concept")
    ytick = np.arange(0,40,1)
    ax.set_yticks(ytick, minor=True)
    ax.grid('off', which='major', axis='y', linestyle='--', linewidth=0.5)
    ax.grid('on', which='minor', axis='y', linestyle=':', linewidth=0.5)

        # plot concept flight movements

    plt.figure(3, figsize=(35, 8))
    plt.title("Total Daily Flight Movements per Concept")

    flights_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='D'), 'current_concept']).size().reset_index()
    flights_hourly.columns = ['timestamp', 'current_concept', 'count']

    for cp in flights_hourly.current_concept.unique():
        conc_ = flights_hourly[flights_hourly.current_concept == cp][['timestamp', 'count']]
        # conc_ = conc_[conc_['count'] > 20]
        print(conc_)

        plt.plot(conc_['timestamp'].values, conc_['count'].values, label=cp)
    # plt.axhline(y=50, xmin=0.0, xmax=1.0, color='r')
    plt.legend()
    ax = plt.gca()
    ytick = np.arange(0, 700, 10)
    ax.set_yticks(ytick, minor=True)
    ax.grid('off', which='major', axis='y', linestyle='--', linewidth=0.5)
    ax.grid('on', which='minor', axis='y', linestyle=':', linewidth=0.5)
    # axes.set_ylim([20, 100])




    # grouping by hour

    flights_hourly = df.set_index("timestamp").groupby([pd.Grouper(freq='H')]).size().reset_index()
    flights_hourly.columns = ['timestamp', 'count']
    flights_hourly['hour'] = flights_hourly['timestamp'].dt.hour



    # sort hourly flights

    percentile = percentile/100
    cutoff = flights_hourly['count'].quantile(percentile)
    sorted_flights_hourly = flights_hourly[flights_hourly['count'] > cutoff].drop('hour', 1)
    sorted_flights_hourly.columns = ['timestamp', 'fl_mov']

    # print(sorted_flights_hourly)

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


    # loitering sorting

    # loitering = pd.DataFrame()
    #
    # for file in os.listdir(os.getcwd() + f"\\data\\arrival_postprocessed"):
    #     if file[-4:] == ".csv":
    #         loit_ = pd.read_csv(
    #             f"data\\arrival_postprocessed\\{file}"
    #         )
    #
    #     loit_ = loit_[loit_['usefull'] == True]
    #     loit_ = loit_[loit_['loitering'] == 1]
    #
    #     loit_['timestamp'] = pd.to_datetime(loit_['timestamp'])
    #     loit_ = loit_.set_index('timestamp').groupby([pd.Grouper(freq='H')]).size().reset_index()
    #     loit_.columns = ['timestamp', 'count']
    #
    #     if len(loit_.index) == 1:
    #         total_timestamps = loit_['count'].sum()
    #         loit_['count'] = loit_['count'] / total_timestamps
    #
    #     elif len(loit_.index) == 2:
    #         total_timestamps = loit_['count'].sum()
    #         loit_['count'] = loit_['count'] / total_timestamps
    #         loit_ = loit_[loit_['count'] > 0.2]
    #
    #     loitering = pd.concat([loitering, loit_], ignore_index=True)
    #
    # loitering.to_csv('loitering.csv', index=False)



    #final dataframe

    def mpl_active_bounds(ax):
        def on_xlims_change(event_ax):
            limits = "new x-axis limits: " + '"' + mpl.dates.num2date(event_ax.get_xlim()[0]).strftime(
                "%Y-%m-%d %H:%M:%S+00:00") + '","' + mpl.dates.num2date(event_ax.get_xlim()[1]).strftime(
                "%Y-%m-%d %H:%M:%S+00:00") + '"'
            print(limits)

        ax.callbacks.connect("xlim_changed", on_xlims_change)

        # import and merge datasets

    loitering['timestamp'] = pd.to_datetime(loitering['timestamp'])

    go_arounds = go_arounds.merge(concept_devs, how='outer', on='timestamp')
    loitering = loitering.merge(go_arounds, how='outer', on='timestamp')
    loitering = loitering.set_index('timestamp').fillna(0)
    loitering.columns = ['loit', 'go_ar', 'con_dev']
    loitering = loitering.reset_index().groupby('timestamp').sum()

    sorted_flights_hourly = sorted_flights_hourly.merge(loitering, how='outer', on='timestamp')

        # define final dataframe, clean and normalize datasets

    final = sorted_flights_hourly
    final = final.loc[final['timestamp'].between(start_date, end_date, inclusive=True)].set_index('timestamp').fillna(0)
    final['fl_mov_norm'] = final['fl_mov'] / cutoff
    final['loit'] = final['loit'] / statistics.mean(final['loit'])
    final['con_dev'] = final['con_dev'] / statistics.mean(final['con_dev'])
    final['total'] = final['loit'] + final['fl_mov_norm'] + final['con_dev'] + final['go_ar']
    final = final.drop('fl_mov', 1).reset_index()


        # final plot

    final.plot.scatter(x='timestamp', y='total', c='total', s=25, cmap=mpl.cm.plasma)
    plt.title("Total Hourly Capacity Markers, {}th percentile".format(percentile))


    ax = plt.gca()
    ytick = np.arange(0,60,1)
    ytick2 = np.arange(0,60,5)
    ax.set_yticks(ytick2, minor=False)
    ax.set_yticks(ytick, minor=True)
    ax.grid('on', which='minor', axis='y', linestyle=':', linewidth=0.5)
    ax.grid('on', which='major', axis='y', linestyle='--', linewidth=0.5)


    xfmt = mpl.dates.DateFormatter("%Y-%m-%d %H:%M:%S")
    ax.xaxis.set_major_formatter(xfmt)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    mpl_active_bounds(ax)

        # sort concept data by critical moments



    plt.show()


data_processor("2019-10-01","2019-11-30",99)