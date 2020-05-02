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
        lst2.append([date,days[i]])
    else:
        if i % 6 == 0: #and lst2[i-1][1] is not 'tuesday':
            lst2.append([date,'tuesday'])
        elif i % 7 == 0: #and lst2[i-1][1] is not 'wednesday':
            lst2.append([date,'wednesday'])
        elif i % 8 == 0: #and lst2[i-1][1] is not 'thursday':
            lst2.append([date,'thursday'])
        elif i % 9 == 0: #and lst2[i-1][1] is not 'friday':
            lst2.append([date,'friday'])
        elif i % 10 == 0: #and lst2[i-1][1] is not 'saturday':
            lst2.append([date,'saturday'])
        elif i % 11 == 0: #and lst2[i-1][1] is not 'sunday':
            lst2.append([date,'sunday'])
        elif i % 12 == 0: #and lst2[i-1][1] is not 'monday':
            lst2.append([date,'monday'])



print(lst2)