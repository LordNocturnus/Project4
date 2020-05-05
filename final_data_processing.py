import pandas as pd
from datetime import datetime
from textwrap import wrap
import matplotlib
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt


def data_processor(start_date, end_date, percentile):
    # data importing
    df = pd.read_csv("data/concept_analysis/concept_analysis.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # print(df)

    # getting rid of old runway data, cleaning up names and stuff
    df = df.rename({'new_runway': 'runway'}, axis=1)
    df = df.drop('initial_runway', 1)
    df = df.drop('icao24', 1)
    df = df.drop('flight_id', 1)
    df['runway'] = df[['runway', 'scheduled_concept', 'current_concept']].astype(int)
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

    # sort concept deviations
    sorted_concept_stuff = df[(df['scheduled_concept'] != df['current_concept']) & (df['scheduled_concept'] != 'Unscheduled')]
    sorted_concept_stuff = sorted_concept_stuff[['timestamp', 'scheduled_concept', 'current_concept']]
    print(sorted_concept_stuff)


data_processor("2019-10-01","2019-11-30",90)