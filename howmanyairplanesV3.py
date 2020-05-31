import pandas as pd
import re

flights = pd.read_csv("data\\useful_flights.csv", dtype= {'icao24':str, 'arriving':bool}).sort_values(by=['timestamp'])

aircraft_db = pd.read_csv("data\\aircraft_db.csv", dtype= {'icao24':str})
# Filter on aircraft type (commercial/non-commercial)

flights = pd.merge(flights, aircraft_db, how='outer', on='icao')

flights = flights.dropna(subset=['flight_id'])

commercial_flights = flights.dropna(subset=['mdl'])
commercial_flights = commercial_flights.loc[commercial_flights.mdl.str.contains('[ab]\\d{3}', case=True, regex=True)]

non_commercial_flights = flights.set_index('icao')
non_commercial_flights = non_commercial_flights.drop(index=commercial_flights.icao)
non_commercial_flights = non_commercial_flights.reset_index()

##### SET ANALYSIS HERE
flights = non_commercial_flights
file = "ground_usage_non_commercial.csv"
##### SET ANALYSIS HERE

## determine how many airplanes are initially @zurich
initial_amount = 0

icaos = set(flights['icao'])
icao_list = flights
icao_list = icao_list.set_index(['icao'])

for icao in icaos:

    if len(icao_list.loc[icao].shape) > 1:

        if icao_list.loc[icao]['arriving'].iloc[0] == False:
            initial_amount += 1
            #print('yes!, ' , icao)

    else:

        if icao_list.loc[icao]['arriving'] == False:
            initial_amount += 1
            #print('yes2!, ' , icao)


print(initial_amount, '/', len(icaos))

#check for everytimestamp how many airplanes there are on zurich
amount = initial_amount
#amount = 70
finallist = []

for i, flight in flights.iterrows():
    timestamp = flight['timestamp']
    if flight['arriving'] == True:
        amount += 1
    elif flight['arriving'] == False:
        amount -= 1
        #if amount <0:
        #    amount = 0
        
    entry = [timestamp, amount]
    finallist.append(entry)

row = ['timestamp', 'amount']
finalpanda = pd.DataFrame(finallist, columns=row)
finalpanda.to_csv(f"data\\runway_usage\\{file}",index=False)
print('done')
'''  
#print(finallist)
time = []
amounts = []

for i in range(0,len(finallist),1000):
    time.append(i)
    amounts.append(finallist[i][1])

pp.plot(time,amounts)
pp.show()
'''
