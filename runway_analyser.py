''' File for working on runway stuff'''

import pandas as pd
import os

runways = []

## ARRIVALS
for folder in os.listdir(os.getcwd() + '\\data\\arrival_flights'): # Folders
    for file in os.listdir(os.getcwd() + '\\data\\arrival_flights\\' + folder): # Flights
        if file[-4:] == '.csv': # Making sure we can do something with this file

            flight = pd.read_csv("data\\arrival_flights\\" + folder + "\\" + file)

            if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                runway = [int(list(flight["runway"])[-1]), list(flight["timestamp"])[-1]]
                runways.append(runway)
                # Dit is dus je runway + de timestamp van landen.

            print(runway)

## DEPARTURES
for folder in os.listdir(os.getcwd() + '\\data\\departure_flights'):
    for file in os.listdir(os.getcwd() + '\\data\\departure_flights\\' + folder):
        if file[-4:] == '.csv':

            flight = pd.read_csv("data\\departure_flights\\" + folder + "\\" + file)

            if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                runway = [int(flight["runway"][0]), list(flight["timestamp"])[0]]
                runways.append(runway)
                # Dit is dus je runway + de timestamp van landen.

            print(runway)