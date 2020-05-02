'''Actual concept finder'''

import pandas as pd

runway10_28 = pd.read_csv("data\\runway_usage\\runway10_28.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")
runway14_32 = pd.read_csv("data\\runway_usage\\runway14_32.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")
runway16_34 = pd.read_csv("data\\runway_usage\\runway16_34.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")

print('import ok')

probable_concept = []

for i, row in runway14_32.iterrows():
    if row['arriving'] == True:
        probable_concept.append([row['timestamp'], 0])

for i, row in runway10_28.iterrows():
    if row['arriving'] == True:
        probable_concept.append([row['timestamp'], 1])

for i, row in runway16_34.iterrows():
    if row['arriving'] == True:
        probable_concept.append([row['timestamp'], 2])

print('concepts analysed')

pandacolumns = ['timestamp', 'concept']

x = pd.DataFrame(probable_concept, columns=pandacolumns).sort_values(by="timestamp")
x.to_csv("data\\actual_concept.csv", index=False)