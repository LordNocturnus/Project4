''' File for working on runway stuff'''

import pandas as pd
import os
#import numpy as np
import math
from statistics import mean, mode
from collections import Counter
from random import random

runways = []

doImport = False

if doImport:

    ## ARRIVALS
    for folder in os.listdir(os.getcwd() + '\\data\\arrival_flights'): # Folders
        for file in os.listdir(os.getcwd() + '\\data\\arrival_flights\\' + folder): # Flights
            if file[-4:] == '.csv': # Making sure we can do something with this file

                flight = pd.read_csv("data\\arrival_flights\\" + folder + "\\" + file, dtype = {'icao24':str, 'arriving':bool, 'timestamp':str})

                if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                    runway = flight.iloc[-1, [-1,-2,5,0]].tolist() #, flight.iloc[-1, -2], flight.iloc[-1,5], flight.iloc[-1,0], True]

                    heading = math.degrees(math.atan2( flight.iloc[-10,8] - flight.iloc[-30,8],
                                                              flight.iloc[-10,7] - flight.iloc[-30,7]))+10
                    if heading <0:
                        heading = heading +360

                    runway.extend([True, [heading]])
                    runways.append(runway)


    print("halfway importing")

    ## DEPARTURES
    for folder in os.listdir(os.getcwd() + '\\data\\departure_flights'):
        for file in os.listdir(os.getcwd() + '\\data\\departure_flights\\' + folder):
            if file[-4:] == '.csv':

                flight = pd.read_csv("data\\departure_flights\\" + folder + "\\" + file, dtype = {'icao24':str, 'arriving':bool, 'timestamp':str})

                if flight.iloc[0,10] > 0 :
                    flight = flight.loc[flight.onground < 1]

                if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                    #runway = [int(flight["runway"][0]), list(flight["flight_id"])[0], list(flight["icao24"])[0], list(flight["timestamp"])[0], False]

                    runway = flight.iloc[-1, [-2, -1, 7, 0]].tolist()

                    #for i in range(0,50,10)

                    headings = []

                    for i in range(10,50):
                        temp_heading = math.degrees(math.atan2(flight.iloc[i+1, 9] - flight.iloc[i, 9],
                                                    flight.iloc[i+1, 8] - flight.iloc[i, 8])) + 10
                        if temp_heading < 0:
                            temp_heading = temp_heading + 360

                        headings.append(temp_heading)

                    mean_heading = mean(headings)

                    #heading = math.degrees(math.arctan2(flight.iloc[30, 9] - flight.iloc[10, 9],
                    #                                flight.iloc[30, 8] - flight.iloc[10, 8])) + 10


                    runway.extend([False, headings])

                    #print(runway)
                    runways.append(runway)

    print('import complete')

    panda_columns = ['runway', 'flight_id', 'icao24', 'timestamp', 'arriving', 'heading']
    all_runways = pd.DataFrame(runways, columns=panda_columns).sort_values(by="timestamp")

    all_runways.to_csv('data\\runway_usage\\all_runways.csv', index=False)

else:
    all_runways = pd.read_csv("data\\runway_usage\\all_runways.csv", dtype = {'icao24':str, 'arriving':bool, 'heading':object})##.sort_values(by=["timestamp"])

for i,row in all_runways.iterrows():

    headings = row['heading'][1:-1].split(", ")

    headings = list(map(float, headings))

    faulty_runways = []
    runways = []

    for heading in headings:
        #heading = float(heading)
        if 80 < heading < 120:
            runways.append(10)
        elif 260 < heading < 300:
            runways.append(28)

        elif 120 < heading < 150:
            runways.append(14)
        elif 300 < heading < 330:
            runways.append(32)

        elif 150 < heading < 180:
            runways.append(16)
        elif 330 < heading < 360:
            runways.append(34)

        else:
            faulty_runways.append(99)

    if len(runways) == 1:
        all_runways.loc[i,'new_runway'] = runways[0]

    elif len(runways) > 1:

        cnt = Counter(runways)

        all_runways.loc[i,'new_runway'] = cnt.most_common()[0][0]

    else:
        all_runways.loc[i,'new_runway'] = 99

'''
all_runways.loc[ (80 < all_runways['heading']) & (all_runways['heading'] < 120) , 'new_runway'] = 10
all_runways.loc[ (250 < all_runways["heading"]) & (all_runways['heading'] < 300) , 'new_runway'] = 28
all_runways.loc[ (120 < all_runways["heading"]) & (all_runways['heading'] < 150) , 'new_runway'] = 14
all_runways.loc[ (300 < all_runways["heading"]) & (all_runways['heading'] < 330) , 'new_runway'] = 32
all_runways.loc[ (150 < all_runways["heading"]) & (all_runways['heading'] < 190) , 'new_runway'] = 16
all_runways.loc[ (330 < all_runways["heading"]) & (all_runways['heading'] < 360) , 'new_runway'] = 34
all_runways.loc[ ((190 < all_runways["heading"]) & (all_runways['heading'] < 250))
                            | ((0 < all_runways["heading"]) & (all_runways['heading'] < 80))
                            | (all_runways["heading"] > 360) , 'new_runway'] = all_runways.loc[:,'runway']

print('assigned runway numbers')

outliers = all_runways.loc[ ((190 < all_runways["heading"]) & (all_runways['heading'] < 250))
                            | ((0 < all_runways["heading"]) & (all_runways['heading'] < 80))
                            | (all_runways["heading"] > 360)]
'''
runway10 = all_runways.loc[all_runways['new_runway'] == 10]
runway14 = all_runways.loc[all_runways['new_runway'] == 14]
runway16 = all_runways.loc[all_runways['new_runway'] == 16]
runway28 = all_runways.loc[all_runways['new_runway'] == 28]
runway32 = all_runways.loc[all_runways['new_runway'] == 32]
runway34 = all_runways.loc[all_runways['new_runway'] == 34]
outliers = all_runways.loc[all_runways['new_runway'] == 99]

#outliers.loc[:,'new_runway'] = 0

runway10_28 = runway10.append(runway28).sort_values(by="timestamp")
runway14_32 = runway14.append(runway32).sort_values(by="timestamp")
runway16_34 = runway16.append(runway34).sort_values(by="timestamp")
outliers = outliers.sort_values(by="timestamp")

print('split and sorted runways')

if "runway_usage" not in os.listdir(os.getcwd() + "\\data"):
    os.mkdir(f"data\\runway_usage")

runway10_28.to_csv('data\\runway_usage\\runway10_28.csv', index=False)
runway14_32.to_csv('data\\runway_usage\\runway14_32.csv', index=False)
runway16_34.to_csv('data\\runway_usage\\runway16_34.csv', index=False)
outliers.to_csv('data\\runway_usage\\outliers.csv', index=False)

print('all written down!')

all_runways.loc[all_runways['runway']!=all_runways['new_runway']].to_csv('data\\runway_usage\\modified_flights.csv', index=False)