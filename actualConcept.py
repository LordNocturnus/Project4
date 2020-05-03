'''Actual concept finder part 2.'''

import pandas as pd

runway_usage = pd.read_csv("data\\probable_concepts.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")

print('import ok')
print('Moving on to find concept switches...')

