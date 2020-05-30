'''Actual concept finder part 2.'''

import pandas as pd

runway_usage = pd.read_csv("data\\probable_concepts.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by=["timestamp"])

print(runway_usage)

print('import ok')

#runway_usage['next_concept'] = runway_usage['concept'].shift(+1)

arriving_flights = runway_usage.loc[runway_usage['arriving']==True]

arriving_flights['next_concept'] = arriving_flights['concept'].shift(+1)

runway_usage = arriving_flights.append(runway_usage.loc[runway_usage['arriving']==False]).sort_values(by=["timestamp"])

print('moving on to find concept switches...')

time_of_switch = [] #pd.DataFrame([], columns=['concept', 'timestamp'])
current_concept = None
failures = 0
total = 0

for i, row in runway_usage.iterrows():
    if current_concept != row['concept'] and row['arriving'] == True and row['next_concept'] != current_concept:
        current_concept = row['concept']
        time_of_switch.append([current_concept, failures, total, row['timestamp']])
        failures = 0
        total = 0

    if row['concept'] == current_concept:
        match = True
    elif row['concept'] == 0.12:
        match = True
    elif row['concept'] == 12 and current_concept != 0:
        match = True
    else:
        match = False
        failures += 1
    total += 1

    runway_usage.loc[i, 'match'] = match
    runway_usage.loc[i, 'current_concept'] = current_concept

print('concept switches and matches found.')

concept_switches = pd.DataFrame(time_of_switch, columns=['concept', 'failures', 'total', 'timestamp'])

runway_usage.to_csv("data\\actual_concepts.csv", index=False)

concept_switches.to_csv("data\\concept_switches.csv", index=False)
