import pandas as pd
import numpy as np


#definitions
def arraytolist(array):
    lst = []
    for i in range(len(array)):
        a = list(array[i])
        lst.append(a)
    return lst


def GetDates(lekker):
    dates = []
    for i in range(len(lekker)):
        timestamp = lekker[i][1]
        string = str(timestamp)
        date = string[0:10]
        dates.append(date)
        b = set(dates)
        realdates = sorted(list(b))
    return realdates


# Read data and sort them by day
#aircrafts14 = np.array(pd.read_csv("data\\runway14_32.csv"))
aircrafts10 = arraytolist(np.array(pd.read_csv("data\\runway_usage\\runway10_28.csv")))
aircrafts14 = arraytolist(np.array(pd.read_csv("data\\runway_usage\\runway14_32.csv")))
aircrafts16 = arraytolist(np.array(pd.read_csv("data\\runway_usage\\runway16_34.csv")))

flights = sorted(aircrafts10 + aircrafts14 + aircrafts16, key=lambda aircraftsitem: aircraftsitem[1])
#sorted(runwaylst, key=lambda runwaylstitem: runwaylstitem[1])
dates = GetDates(flights)
#print(str(flights[0][2]))
#print(len(dates))
# arrivals


#departure


## determine how many airplanes are initially @zurich

initial_amount = 0
icao_list = pd.read_csv("data\\icao24.csv", dtype= {'icao24':str, 'arriving':bool})

icaos = set(icao_list['icao24'])

icao_list = icao_list.set_index(['icao24'])
print(icao_list.loc['0083c3'])
print(icao_list.loc['0083c3'].iloc[0]['arriving'])
print(icao_list.loc['0083c3'].shape)

for icao in icaos:

    if len(icao_list.loc[icao].shape) > 1:

        if icao_list.loc[icao]['arriving'].iloc[0] == False:
            initial_amount += 1
            print('yes!, ' , icao)

    else:

        if icao_list.loc[icao]['arriving'] == False:
            initial_amount += 1
            print('yes2!, ' , icao)


print(initial_amount, '/', len(icaos))

# check all airplanes per day, if arriving --> amount+=1 else amount-=1

finallist = []
dayamount = [Ninit]
for i in range(len(flights)-1):
    amount = dayamount[i-1]
    flightdatestring = str(flights[i][1])
    flightdate = flightdatestring[0:10]
    nextflightdatestring = str(flights[i + 1][1])
    nextflightdate = nextflightdatestring[0:10]
    if flightdate == nextflightdate:
        if flights[i][4] == True:
            amount += 1
            dayamount.append(amount)
        else:
            amount -= 1
            dayamount.append(amount)
        print('amount:', amount)
    print('day:' , dayamount)

    #daycapacity = max(dayamount)
    #entry = [date,daycapacity]
    #finallist.append(entry)

#print(finallist)
#print(len(finallist))