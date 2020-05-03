'''Actual concept finder'''

import pandas as pd

runway10_28 = pd.read_csv("data\\runway_usage\\runway10_28.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")
runway14_32 = pd.read_csv("data\\runway_usage\\runway14_32.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")
runway16_34 = pd.read_csv("data\\runway_usage\\runway16_34.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by="timestamp")

print('import ok')

probable_concept = []
errors = 0

for i, row in runway14_32.iterrows():
    if row['arriving'] == True and row['runway'] == 14:
        concept = 0
    elif row['arriving'] == False and row['runway'] == 32:
        concept = 12
    else:
        concept = 99
        errors += 1
    runway14_32.loc[i,'concept'] = concept

print('analysed runway 14/32')

for i, row in runway10_28.iterrows():
    if row['arriving'] == True and row['runway'] == 28:
        concept = 1
    elif row['arriving'] == False and row['runway'] == 10:
        concept = 0
    elif row['arriving'] == False:
        concept = 0.12
    else:
        concept = 99
        errors += 1
    runway10_28.loc[i,'concept'] = concept

print('analysed runway 10/28')

for i, row in runway16_34.iterrows():
    if row['arriving'] == True and row['runway'] == 34:
        concept = 2
    elif row['arriving'] == False and row['runway'] == 16:
        concept = 0
    elif row['arriving'] == False:
        concept = 12
    else:
        concept = 99
        errors += 1
    runway16_34.loc[i,'concept'] = concept

print('analysed runway 16/34')

print(f'concepts analysed with {errors} errors.')

probable_concept = runway16_34.append(runway10_28).append(runway14_32).sort_values(by="timestamp")

#x = pd.DataFrame(probable_concept).sort_values(by="timestamp")
probable_concept.to_csv("data\\probable_concepts.csv", index=False)