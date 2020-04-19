### Aircraft turnaround calculator

import pandas as pd
from datetime import datetime
import statistics
import matplotlib.pyplot as plt

aircrafts = pd.read_csv("data\\icao24.csv", dtype = {'icao24':str, 'arriving':bool})

aircrafts['icao24_s'] = aircrafts['icao24'].shift(-1)
aircrafts['timestamp_s'] = aircrafts['timestamp'].shift(-1)
aircrafts['arriving_s'] = aircrafts['arriving'].shift(-1)

double_arrivals = 0
double_departures = 0

for i, aircraft in aircrafts.iterrows():
    #print(aircraft['arriving'],aircraft['arriving_s'],aircraft['icao24'],aircraft['icao24_s'])

    if aircraft['icao24'] == aircraft['icao24_s']:
        if aircraft['arriving'] == True and aircraft['arriving_s'] == True:
            double_arrivals += 1
        elif aircraft['arriving'] == False and aircraft['arriving_s'] == False:
            double_departures += 1

print(double_arrivals, double_departures)

