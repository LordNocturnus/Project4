### File for extracting list of icao24

import pandas as pd
import os

aircraft = []

for folder in os.listdir(os.getcwd() + '\\data\\arrival_flights'): # Folders
    for file in os.listdir(os.getcwd() + '\\data\\arrival_flights\\' + folder): # Flights
        if file[-4:] == '.csv': # Making sure we can do something with this file

            flight = pd.read_csv(f"data\\arrival_flights\\{folder}\\{file}", dtype = {'icao24':str})

            entry = [list(flight["icao24"])[-1], list(flight["flight_id"])[-1], list(flight["timestamp"])[-1], True]

            #print(entry)

            aircraft.append(entry)

print("halfway!")

for folder in os.listdir(os.getcwd() + '\\data\\departure_flights'): # Folders
    for file in os.listdir(os.getcwd() + '\\data\\departure_flights\\' + folder): # Flights
        if file[-4:] == '.csv': # Making sure we can do something with this file

            flight = pd.read_csv(f"data\\departure_flights\\{folder}\\{file}", dtype = {'icao24':str})

            entry = [list(flight["icao24"])[-1], list(flight["flight_id"])[-1], list(flight["timestamp"])[0], False]

            #print(entry)

            aircraft.append(entry)

aircraft = sorted(sorted(aircraft, key=lambda aircraftitem: aircraftitem[1]), key=lambda aircraftitem: aircraftitem[0])

aircraft_pandas = pd.DataFrame(aircraft, columns =['icao24', 'flight_id', 'timestamp', 'arriving'])
aircraft_pandas.to_csv('data\\icao24.csv', index=False)