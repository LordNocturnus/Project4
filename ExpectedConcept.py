import pandas as pd

flights = pd.read_csv("data\\addeddayforexpectedconcept.csv")

#print(flights)
# North concept, Mon-Fri [7-21), Sat-Sun [9-20) : 0
# East concept, Mon-Fi [21 - 2330], Sat-Sun [20-2330]: 1
# South concept, Mor-Fri [6-7), Sat-Sun [6-9): 2
lst = []
for i, flight in flights.iterrows():
    day = flight['day']
    hour = flight['timestamp'][0:2]
    inthour = int(hour)
    minute = flight['timestamp'][3:5]
    intminute = int(minute)
    wantedtimestamp = flight['date'] + ' '+ flight['timestamp']
    if inthour in range(0,6):
        lst.append([wantedtimestamp,99])

    elif inthour == 23:
        if intminute in range(31,60):
            lst.append([wantedtimestamp,99])



    elif (day is not 'sat' and day is not 'sun'):
        if inthour in range(7,21):
            lst.append([wantedtimestamp, 0])
        elif inthour in range(21,23):
            lst.append([wantedtimestamp,1])
        elif inthour == 23:
            if intminute in range(0,31):
                lst.append([wantedtimestamp,1])
        elif inthour in range(6,7):
            lst.append([wantedtimestamp,2])


    elif (day == 'sat' or day == 'sun'):
        if inthour in range(9,20):
            lst.append([wantedtimestamp,0])
        elif inthour in range(20,23):
            lst.append([wantedtimestamp,1])
        elif inthour == 23:
            if intminute in range(0,31):
                lst.append([wantedtimestamp,1])
        elif inthour in range(6-9):
            lst.append([wantedtimestamp,2])

expectedcolumns = ['timestamp','ExpectedConcept']
expectedlist = pd.DataFrame(lst,columns=expectedcolumns) #This dataframe has 1 flight less then the original amount of flights
expectedlist.to_csv("data\\expected_concept.csv",index=False)
print('done')



