'''Actual concept finder'''

import pandas as pd

runway10_28 = pd.read_csv("data\\runway_usage\\runway10_28.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")
runway14_32 = pd.read_csv("data\\runway_usage\\runway14_32.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")
runway16_34 = pd.read_csv("data\\runway_usage\\runway16_34.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")

print('import ok')

if runway10_28['arriving'] == True:
