import numpy as np
import pandas as pd
import pyarrow.parquet as pq

data_arrival = pq.read_table("data/arrival_dataset.parquet")
#data_departure = pq.read_table("data/departure_dataset.parquet")

data_arrival = data_arrival.to_pandas()
#data_departure = data_departure.to_pandas()

flights = set(data_arrival["callsign"])

print("Found", len(flights), "different aircraft for arrival")
for flight in flights:
    temp = pd.DataFrame(columns=data_arrival.columns)
    indices = data_arrival[data_arrival["callsign"] == flight].index.tolist()
    print(len(indices))
    print(flight, data_arrival.iloc[indices[0]]["callsign"])
    #for row in data_arrival.row:
    #    if row["callsign"] == flight:
    #        temp.append(row)

