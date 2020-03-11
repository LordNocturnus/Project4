import numpy as np
import pandas as pd
import pyarrow.parquet as pq

data_arrival = pq.read_table("data/arrival_dataset.parquet")
#data_departure = pq.read_table("data/departure_dataset.parquet")

data_arrival = data_arrival.to_pandas()
#data_departure = data_departure.to_pandas()