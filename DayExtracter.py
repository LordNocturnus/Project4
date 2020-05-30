import pandas as pd

def GetDates(lekker):
    dates = []
    for i in range(len(lekker)):
        dates.append(lekker[i])
    y = sorted(set(dates))
    return y

#flights = pd.read_csv("data\\useful_flights.csv", dtype= {'icao24':str, 'arriving':bool}).sort_values(by=['timestamp'])
flights = pd.read_csv("data\\weatherdata.csv").sort_values(by=['timestamp'])

lst = []
for i,flight in flights.iterrows():
    date = flight['timestamp'][0:10]
    time = flight['timestamp'][11:19]
    entry = [date,time,flight['direction']]
    lst.append(entry)

newcolumns = ['date','time', 'direction']
newflights = pd.DataFrame(lst,columns=newcolumns)


#1 oktober=dinsdag
days = ['tuesday','wednesday','thursday','friday','saturday','sunday','monday']
dates = GetDates(newflights['date'])
lst2 = []
for i in range(len(dates)):
    date = dates[i]
    if i % 7 == 0:
        lst2.append([date,'tue'])
    elif i % 7 == 1:
        lst2.append([date,'wed'])
    elif i % 7 == 2:
        lst2.append([date,'thu'])
    elif i % 7 == 3:
        lst2.append([date,'fri'])
    elif i % 7 == 4:
        lst2.append([date,'sat'])
    elif i % 7 == 5:
        lst2.append([date,'sun'])
    elif i % 7 == 6:
        lst2.append([date,'mon'])

dayscolumns = ['date', 'day']
daysDF = pd.DataFrame(lst2,columns=dayscolumns)
#print(daysDF)
lst3 = []
for i, time in daysDF.iterrows():
    date = time['date']
    day = time['day']
    for j, flight in newflights.iterrows():
        if date == flight['date']:
            lst3.append([flight['date'], day, flight['time'], flight['direction']])

lastcolumns = ['date', 'day', 'timestamp', 'direction']
panda = pd.DataFrame(lst3, columns=lastcolumns)
panda.to_csv("data\\AddedWindDirection.csv", index=False)
print('done')

