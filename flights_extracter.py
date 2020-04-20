import pandas as pd


flights = pd.read_csv("data\\icao24.csv", dtype= {'icao24':str, 'arriving':bool})
flights['next_icao'] = flights['icao24'].shift(+1)
flights['next_arriving'] = flights['arriving'].shift(+1)
flights['last_arriving'] = flights['arriving'].shift(-1)

useless = 0
usefull = []
for i, flight in flights.iterrows():
    if flight['icao24'] == flight['next_icao']:
        if ((flight['arriving'] == True and flight['next_arriving'] == True) or (flight['arriving'] == False and flight['next_arriving'] == False)) or ((flight['arriving'] == True and flight['last_arriving'] == True) or (flight['arriving'] == False and flight['last_arriving'] == False)) :
            useless += 1

        else:
            entry = [flight['icao24'], flight['flight_id'], flight['timestamp'], flight['arriving']]
            usefull.append(entry)

pandacolumns = ['icao', 'flight_id', 'timestamp', 'arriving']

x = pd.DataFrame(usefull, columns=pandacolumns)
x.to_csv("data\\usefullflights.csv", index=False)
print(useless, 'done')