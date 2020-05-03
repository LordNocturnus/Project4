from flight_plotter import part_of_flights
from runway_usage import part_of_total_flights
from aircraft_parking import *
import matplotlib.pyplot as plt

plt.figure(figsize=(16,9))

start,end = "2019-11-14 10:55:15+00:00","2019-11-15 12:26:40+00:00"
truncate_val = 30
percentile_val = 67

part_of_flights(start,end,231)
part_of_aircraft_parking(start,end,232)
part_of_total_flights(start, end, 233, truncate_val, percentile_val)

plt.show()
