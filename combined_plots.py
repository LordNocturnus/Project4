from flight_plotter import part_of_flights
from aircraft_parking import *
import matplotlib.pyplot as plt

plt.figure(figsize=(16,9))

start,end = "2019-11-14 10:55:15+00:00","2019-11-15 12:26:40+00:00"
part_of_flights(start,end,121)
part_of_aircraft_parking(start,end,122)
#We will have to input this into each subplot

plt.show()
