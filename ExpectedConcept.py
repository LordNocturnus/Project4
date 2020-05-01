import pandas as pd

def GetDates(lekker):
    dates = []
    for i in range(len(lekker)):
        dates.append(lekker[i])
    x =set(dates)
    y = sorted(x)
    return y

flights = pd.read_csv("data\\useful_flights.csv", dtype= {'icao24':str, 'arriving':bool}).sort_values(by=['timestamp'])

lst = []
for i,flight in flights.iterrows():
    date = flight['timestamp'][0:10]
    time = flight['timestamp'][11:19]
    entry = [date,time]
    lst.append(entry)

newcolumns = ['date','time']
newflights = pd.DataFrame(lst,columns=newcolumns)


#1 oktober=dinsdag
days = ['tuesday','wednesday','thursday','friday','saturday','sunday','monday']
dates = GetDates(newflights['date'])
lst2 = []
for i in range(len(dates)):
    date = dates[i]
    if i <= 6:
        j = i
    else:
        if i % 6 == 0 and lst2[i-1][1] is not 'tuesday':
            j = 0
        elif i % 7 == 0 and lst2[i-1][1] is not 'wednesday':
            j = 1
        elif i % 8 == 0 and lst2[i-1][1] is not 'thursday':
            j = 2
        elif i % 9 == 0 and lst2[i-1][1] is not 'friday':
            j = 3
        elif i % 10 == 0 and lst2[i-1][1] is not 'saturday':
            j = 4
        elif i % 11 == 0 and lst2[i-1][1] is not 'sunday':
            j = 5
        elif i % 12 == 0 and lst2[i-1][1] is not 'monday':
            j = 6



    day = days[j]
    lst2.append([date,day])

print(lst2)