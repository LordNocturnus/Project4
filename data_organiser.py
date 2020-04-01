import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import os


data_arrival = pq.read_table("data/arrival_dataset.parquet")
data_arrival = data_arrival.to_pandas()
flights = set(data_arrival["callsign"])

print("ok")

print("Found", len(flights), "different aircraft for arrival")
if "arrival_processed" not in os.listdir(os.getcwd() + "\\data"):
    os.mkdir("data\\arrival_processed")
for flight in list(flights):
    print(flight, list(flights).index(flight) / len(flights))
    temp = data_arrival[data_arrival["callsign"] == flight]
    temp = temp.sort_values("timestamp")
    temp.to_csv(f'data\\arrival_processed\\{flight}.csv', index=False)

del data_arrival
data_departure = pq.read_table("data/departure_dataset.parquet")
data_departure = data_departure.to_pandas()
flights = set(data_arrival["callsign"])

print("Found", len(flights), "different aircraft for departure")
if "departure_processed" not in os.listdir(os.getcwd() + "\\data"):
    os.mkdir("data\\departure_processed")
for flight in flights:
    print(flight, list(flights).index(flight) / len(flights))
    temp = data_arrival[data_departure["callsign"] == flight]
    temp = temp.sort_values("timestamp")
    temp.to_csv(f'data\\departure_processed\\{flight}.csv', index=False)
