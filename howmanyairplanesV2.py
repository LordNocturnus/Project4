import pandas as pd
import openpyxl
from matplotlib import pyplot as pp

flights = pd.read_csv("data\\useful_flights.csv", dtype= {'icao24':str, 'arriving':bool}).sort_values(by=['timestamp'])

print(flights)

## determine how many airplanes are initially @zurich

initial_amount = 0
icao_list = pd.read_csv("data\\icao24.csv", dtype= {'icao24':str, 'arriving':bool}).sort_values(by=['timestamp'])

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
finalpanda.to_csv("data\\runway_usage\\howmanyairplanes2.csv",index=False)
#finalpanda.to_excel("data\\runway_usage\\howmanyairplanes.xlsx", sheet_name='howmanyairplanes', index=True)
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
