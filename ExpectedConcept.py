import pandas as pd

flights = pd.read_csv("data\\AddedWindDirection.csv")

#print(flights)
# North concept, Mon-Fri [7-21), Sat-Sun [9-20) : 0
# East concept, Mon-Fi [21 - 2330], Sat-Sun [20-2330]: 1
# South concept, Mor-Fri [6-7), Sat-Sun [6-9): 2
lst = []
for i, flight in flights.iterrows():
    date = flight['timestamp'][0:10]
    day = flight['day']
    hour = flight['timestamp'][11:13]
    inthour = int(hour)
    minute = flight['timestamp'][14:16]
    intminute = int(minute)
    wantedtimestamp = flight['timestamp']
    direction = flight['direction']
    flight_id = flight['flight_id']
    if inthour in range(0,6):
        lst.append([wantedtimestamp,flight_id,99])

    elif inthour == 23:
        if intminute in range(31,60):
            lst.append([wantedtimestamp,flight_id,99])

    elif (direction in range(70,111)) and (inthour in range(6,21)): #westerly wind during daytime
        lst.append([wantedtimestamp,flight_id,1])

    elif direction in range(180,271):
        lst.append([wantedtimestamp,flight_id,2])

    elif ((day == 'sat' or day == 'sun') or (date == '2019-10-03' or date == '2019-11-01')) and (direction not in range(70,111) or direction not in range(180,271)): #these are public hollidays in Baden-Würtemmberg according to: https://publicholidays.de/baden-wurttemberg/2019-dates/
        if inthour in range(9,20):
            lst.append([wantedtimestamp,flight_id,0])
        elif inthour in range(20,23):
            lst.append([wantedtimestamp,flight_id,1])
        elif inthour == 23:
            if intminute in range(0,31):
                lst.append([wantedtimestamp,flight_id,1])
        elif inthour in range(6,9):
            lst.append([wantedtimestamp,flight_id,2])




    elif ((day is not 'sat' and day is not 'sun') and (date is not '2019-10-03' or date is not '2019-11-01')) and (direction not in range(70,111) or direction not in range(180,271)):
        if inthour in range(7,21):
            lst.append([wantedtimestamp, flight_id,0])
        elif inthour in range(21,23):
            lst.append([wantedtimestamp,flight_id,1])
        elif inthour == 23:
            if intminute in range(0,31):
                lst.append([wantedtimestamp,flight_id,1])
        elif inthour in range(6,7):
            lst.append([wantedtimestamp,flight_id,2])




expectedcolumns = ['timestamp','flight_id','expected_concept']
expectedlist = pd.DataFrame(lst,columns=expectedcolumns) #This dataframe has 1 flight less then the original amount of flights
expectedlist.to_csv("data\\expected_concept_VFinal.csv",index=False)
print('done')



