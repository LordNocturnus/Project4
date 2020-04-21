import pandas as pd


flights = pd.read_csv("data\\icao24.csv", dtype= {'icao24':str, 'arriving':bool})
flights['next_icao'] = flights['icao24'].shift(+1)
flights['next_arriving'] = flights['arriving'].shift(+1)
flights['last_icao'] = flights['icao24'].shift(-1)
flights['last_arriving'] = flights['arriving'].shift(-1)


useful = []
not_useful = []
for i, flight in flights.iterrows():
    if not (flight['icao24'] == flight['last_icao'] and
            ((flight['arriving'] == True and flight['last_arriving'] == True) or
             (flight['arriving'] == False and flight['last_arriving'] == False))) :

        entry = [flight['icao24'], flight['flight_id'], flight['timestamp'], flight['arriving']]
        useful.append(entry)
    else:
        entry = [flight['last_icao'], flight['last_arriving'], flight['icao24'], flight['arriving'], flight['next_icao'],
             flight['next_arriving']]
        not_useful.append(entry)

pandacolumns = ['icao', 'flight_id', 'timestamp', 'arriving']

x = pd.DataFrame(useful, columns=pandacolumns)
x.to_csv("data\\useful_flights.csv", index=False)

y = pd.DataFrame(not_useful, columns = ['last_icao24', 'last_arriving', 'icao24', 'arriving', 'next_icao24', 'next_arriving'])
y.to_csv("data\\not_useful_flights.csv", index = False)
print('done')