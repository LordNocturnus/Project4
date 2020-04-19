import pandas as pd

flights = pd.read_csv("data\\icao24.csv")

flights['next_icao'] = flights['icao24'].shift(+1)
flights['next_arriving'] = flights['arriving'].shift(+1)
flights['last_arriving'] = flights['arriving'].shift(-1)


## determine how many airplanes are initially @zurich

initial_amount = 0
icao_list = pd.read_csv("data\\icao24.csv", dtype= {'icao24':str, 'arriving':bool})

icaos = set(icao_list['icao24'])

icao_list = icao_list.set_index(['icao24'])
#print(icao_list.loc['0083c3'])
#print(icao_list.loc['0083c3'].iloc[0]['arriving'])
#print(icao_list.loc['0083c3'].shape)

for icao in icaos:

    if len(icao_list.loc[icao].shape) > 1:

        if icao_list.loc[icao]['arriving'].iloc[0] == False:
            initial_amount += 1
            #print('yes!, ' , icao)

    else:

        if icao_list.loc[icao]['arriving'] == False:
            initial_amount += 1
            #print('yes2!, ' , icao)


#print(initial_amount, '/', len(icaos))

#check for everytimestamp how many airplanes there are on zurich
amount = initial_amount
useless = 0
finallist = []
for i, flight in flights.iterrows():
    if flight['icao24'] == flight['next_icao']:
        if ((flight['arriving'] == True and flight['next_arriving'] == True) or (flight['arriving'] == False and flight['next_arriving'] == False)) or ((flight['arriving'] == True and flight['last_arriving'] == True) or (flight['arriving'] == False and flight['last_arriving'] == False)) :
            useless += 1

        else:
            timestamp = flight['timestamp']
            if flight['arriving'] == True:
                amount += 1
            elif flight['arriving'] == False:
                amount -= 1

            entry = [timestamp, amount]
            finallist.append(entry)

print(finallist)



