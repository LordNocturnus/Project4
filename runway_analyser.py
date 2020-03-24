''' File for working on runway stuff'''

import pandas as pd
import os

runways = []

for folder in os.listdir(os.getcwd() + '\\data\\arrival_flights'):
    for file in os.listdir(os.getcwd() + '\\data\\arrival_flights\\' + folder):
        if file[-4:] == '.csv':

            flight = pd.read_csv("data\\arrival_flights\\" + folder + "\\" + file)

            if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                runway = [set(flight["runway"]), list(flight["timestamp"])[-1]]
                runways.append(runway)
                # Dit is dus je runway + de timestamp van landen.

            print(runway)