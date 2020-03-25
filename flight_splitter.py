import numpy as np
import pandas as pd
import os
import sys

for file in os.listdir(os.getcwd() + '\\data\\arrival_processed'):
    if file[-4:] == '.csv':
        if file[:-4] not in os.listdir(os.getcwd() + "\\data\\arrival_processed_2"):
            os.mkdir(f"data\\arrival_processed_2\\{file[:-4]}")

        callsigns = pd.read_csv(f"data\\arrival_processed\\{file}")

        flights = set(callsigns["flight_id"])

        for flight in list(flights):
            # print(flight, list(flights).index(flight) / len(flights))
            temp = callsigns[callsigns["flight_id"] == flight]
            temp = temp.sort_values("timestamp")
            temp.to_csv(f'data\\arrival_processed_2\\{file[:-4]}\\{flight}.csv', index=False)

        print(file)

for file in os.listdir(os.getcwd() + '\\data\\departure_processed'):
    if file[-4:] == '.csv':
        if file[:-4] not in os.listdir(os.getcwd() + "\\data\\departure_processed_2"):
            os.mkdir(f"data\\departure_processed_2\\{file[:-4]}")

        callsigns = pd.read_csv(f"data\\departure_processed\\{file}")

        flights = set(callsigns["flight_id"])

        for flight in list(flights):
            # print(flight, list(flights).index(flight) / len(flights))
            temp = callsigns[callsigns["flight_id"] == flight]
            temp = temp.sort_values("timestamp")
            temp.to_csv(f'data\\departure_processed_2\\{file[:-4]}\\{flight}.csv', index=False)

        print(file)
