### Aircraft turnaround calculator

import pandas as pd
from datetime import datetime
import statistics
import matplotlib.pyplot as plt

aircrafts = pd.read_csv("data\\icao24.csv", dtype = {'icao24':str, 'arriving':bool})
turnaround_times = []
crazy_turnaround_times = []

aircrafts['icao24_s'] = aircrafts['icao24'].shift(-1)
aircrafts['timestamp_s'] = aircrafts['timestamp'].shift(-1)
aircrafts['arriving_s'] = aircrafts['arriving'].shift(-1)

#print(aircrafts)

for i, aircraft in aircrafts.iterrows():
    #print(aircraft['arriving'],aircraft['arriving_s'],aircraft['icao24'],aircraft['icao24_s'])

    if aircraft['arriving'] == True and aircraft['arriving_s'] == False and aircraft['icao24'] == aircraft['icao24_s'] and aircraft['flight_id'][0:3]: #not in ['SWR', 'EDW']: #!= 'SWR' and aircraft['flight_id'][0:3] != 'EDW':
        d1 = datetime.strptime(aircraft['timestamp'][:-6], "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime(aircraft['timestamp_s'][:-6], "%Y-%m-%d %H:%M:%S")

        difference = d2-d1 #datetime.timedelta(d1,d2)

        #print(d1,d2,difference.seconds)
        if difference.seconds in range(0, 18000): #and difference.seconds : #72000 and difference.seconds > 3600:
            turnaround_times.append(difference.seconds)
        else:
            crazy_turnaround_times.append(difference.seconds)

print(sorted(turnaround_times))
print(statistics.mean(turnaround_times), min(turnaround_times), max(turnaround_times), len(turnaround_times))

xx = []
yy = []

for i in range(1000):
    xx.append(18*i)
    yy.append(0)

for turnaround in turnaround_times:
    for i, x in enumerate(xx):
        if turnaround - xx[i] < 900:
            yy[i] += 1
            break

plt.plot(xx,yy)
plt.show()
