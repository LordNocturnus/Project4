import pandas as pd

flights = pd.read_csv("data\\AddedWindDirectionAndSpeed.csv")

kts = 0.539956803 # kts/(km/h)
#print(flights)
# North concept, Mon-Fri [7-21), Sat-Sun [9-20) : 0
# East concept, Mon-Fi [21 - 2330], Sat-Sun [20-2330]: 1
# South concept, Mor-Fri [6-7), Sat-Sun [6-9): 2
lst = []
for i, flight in flights.iterrows():
    date = flight['date']
    day = flight['day']
    hour = flight['timestamp'][0:2]
    inthour = int(hour)
    minute = flight['timestamp'][3:5]
    intminute = int(minute)
    wantedtimestamp = flight['date'] + ' ' + flight['timestamp']
    direction = flight['direction']
    speed = flight['WindSpeed']
    if inthour in range(0,6):
        lst.append([wantedtimestamp,99])

    elif inthour == 23:
        if intminute in range(31,60):
            lst.append([wantedtimestamp,99])

    elif (direction in range(70,111)) and (inthour in range(6,21)) and (kts * speed >= 25): #westerly wind during daytime with a windspeed magnitude bigger than 25 kts
        lst.append([wantedtimestamp,1])

    elif direction in range(180,271) and  (kts * speed >= 25):
        lst.append([wantedtimestamp,2])

    elif ((day == 'sat' or day == 'sun') or (date == '2019-10-03' or date == '2019-11-01')) and (direction not in range(70,111) or direction not in range(180,271)): #these are public hollidays in Baden-Würtemmberg according to: https://publicholidays.de/baden-wurttemberg/2019-dates/
        if inthour in range(9,20):
            lst.append([wantedtimestamp,0])
        elif inthour in range(20,23):
            lst.append([wantedtimestamp,1])
        elif inthour == 23:
            if intminute in range(0,31):
                lst.append([wantedtimestamp,1])
        elif inthour in range(6,9):
            lst.append([wantedtimestamp,2])




    elif ((day is not 'sat' and day is not 'sun') and (date is not '2019-10-03' or date is not '2019-11-01')) and (direction not in range(70,111) or direction not in range(180,271)):
        if inthour in range(7,21):
            lst.append([wantedtimestamp, 0])
        elif inthour in range(21,23):
            lst.append([wantedtimestamp,1])
        elif inthour == 23:
            if intminute in range(0,31):
                lst.append([wantedtimestamp,1])
        elif inthour in range(6,7):
            lst.append([wantedtimestamp,2])




expectedcolumns = ['timestamp','ExpectedConcept']
expectedlist = pd.DataFrame(lst,columns=expectedcolumns) #This dataframe has 1 flight less then the original amount of flights
expectedlist.to_csv("data\\expected_concept_V2Final.csv",index=False)
print('done')



