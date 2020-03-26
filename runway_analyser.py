''' File for working on runway stuff'''

import pandas as pd
import os

runways = []
runway10 = [["runway", "timestamp", "arriving/departing"]]
runway14 = [["runway", "timestamp", "arriving/departing"]]
runway16 = [["runway", "timestamp", "arriving/departing"]]
## ARRIVALS

missing = 0
present = 0

for folder in os.listdir(os.getcwd() + '\\data\\arrival_flights'): # Folders
    for file in os.listdir(os.getcwd() + '\\data\\arrival_flights\\' + folder): # Flights
        if file[-4:] == '.csv': # Making sure we can do something with this file

            flight = pd.read_csv("data\\arrival_flights\\" + folder + "\\" + file)

            if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                runway = [int(list(flight["runway"])[-1]), list(flight["timestamp"])[-1], True]
                realrunway = runway[0]
                if realrunway == 10 or realrunway == 28:
                    runway10.append(runway)

                elif realrunway == 14 or realrunway == 32:
                    runway14.append(runway)

                elif realrunway == 16 or realrunway == 34:
                    runway16.append(runway)

                present += 1

            else:
                missing += 1


                #runways.append(runway) #runways[i][0] is runway, runways [i][1] is timestamp
                # Dit is dus je runway + de timestamp van landen.

            #print(runway)


## DEPARTURES
for folder in os.listdir(os.getcwd() + '\\data\\departure_flights'):
    for file in os.listdir(os.getcwd() + '\\data\\departure_flights\\' + folder):
        if file[-4:] == '.csv':

            flight = pd.read_csv("data\\departure_flights\\" + folder + "\\" + file)

            if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                runway = [int(flight["runway"][0]), list(flight["timestamp"])[0], False]
                realrunway = runway[0]
                if realrunway == 10 or realrunway == 28:
                    runway10.append(runway)

                elif realrunway == 14 or realrunway == 32:
                    runway14.append(runway)

                elif realrunway == 16 or realrunway == 34:
                    runway16.append(runway)

                present += 1

            else:
                missing += 1
                #runways.append(runway)
                # Dit is dus je runway + de timestamp van landen.

#            print(runway)

print("runway 10")
print(runway10)
print('runway 14')
print(runway14)
print("runway 16")
print(runway16)

print(present, missing, missing / (present+missing))


#if "runway_usage" not in os.listdir(os.getcwd() + "\\data"):
#    os.mkdir(f"data\\runway_usage")

#runways = pd.DataFrame(runways, columns =['runway', 'timestamp', 'arriving'])

#runways.to_csv('data\\runway_usage\\test.csv', index=False)

