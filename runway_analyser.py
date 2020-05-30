''' File for working on runway stuff'''

import pandas as pd
import os
import numpy as np

def sort_runway_time(runwaylst):
    #dtype = [['runway',int],['date','S19'],['departing/arriving',bool]]
    #values = runwaylst
    #a = np.array(values,dtype=dtype)
    #x = np.sort(a,order='date')

    return sorted(runwaylst, key=lambda runwaylstitem: runwaylstitem[1])
    #return x

#runways = []
runway10 = []
runway14 = []
runway16 = []
wtf = []
## ARRIVALS
for folder in os.listdir(os.getcwd() + '\\data\\arrival_flights'): # Folders
    for file in os.listdir(os.getcwd() + '\\data\\arrival_flights\\' + folder): # Flights
        if file[-4:] == '.csv': # Making sure we can do something with this file

            flight = pd.read_csv("data\\arrival_flights\\" + folder + "\\" + file, dtype = {'icao24':str, 'arriving':bool, 'timestamp':str})

            if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                runway = [int(flight.iloc[-1, -1]), flight.iloc[-1, -2], flight.iloc[-1,5], flight.iloc[-1,0], True]

                heading = np.degrees(np.arctan2( flight.iloc[-1,8] - flight.iloc[-2,8],
                                                          flight.iloc[-1,7] - flight.iloc[-2,7]))+10
                if heading <0:
                    heading = heading +360

                #print(runway[1])

                realrunway = runway[0]

                runway.append(heading)

                if 80 < heading < 120:
                    runway.append(10)
                    runway10.append(runway)
                elif 260 < heading < 300:
                    runway.append(28)
                    runway10.append(runway)

                elif 120 < heading < 150:
                    runway.append(14)
                    runway14.append(runway)
                elif 300 < heading < 330:
                    runway.append(32)
                    runway14.append(runway)

                elif 150 < heading < 180:
                    runway.append(16)
                    runway16.append(runway)
                elif 330 < heading < 360:
                    runway.append(34)
                    runway16.append(runway)

                else:
                    runway.append(0)
                    wtf.append(runway)

                #elif realrunway == 14 or realrunway == 32:
                #    runway14.append(runway)

                #elif realrunway == 16 or realrunway == 34:
                 #   runway16.append(runway)




                #runways.append(runway) #runways[i][0] is runway, runways [i][1] is timestamp
                # Dit is dus je runway + de timestamp van landen.

            #print(runway)

print("HALFWAY! :d")

## DEPARTURES
for folder in os.listdir(os.getcwd() + '\\data\\departure_flights'):
    for file in os.listdir(os.getcwd() + '\\data\\departure_flights\\' + folder):
        if file[-4:] == '.csv':

            flight = pd.read_csv("data\\departure_flights\\" + folder + "\\" + file, dtype = {'icao24':str, 'arriving':bool, 'timestamp':str})

            if len(set(flight["runway"])) == 1: # We don't have runway information for all flights. This covers situation where that occurs.

                runway = [int(flight["runway"][0]), list(flight["flight_id"])[0], list(flight["icao24"])[0], list(flight["timestamp"])[0], False]
                realrunway = runway[0]

                #print(runway[1])

                heading = np.degrees(np.arctan2(flight.iloc[1, 9] - flight.iloc[0, 9],
                                                flight.iloc[1, 8] - flight.iloc[0, 8])) + 10
                if heading < 0:
                    heading = heading + 360

                runway.append(heading)

                if 80 < heading < 120:
                    runway.append(10)
                    runway10.append(runway)
                elif 260 < heading < 300:
                    runway.append(28)
                    runway10.append(runway)

                elif 120 < heading < 150:
                    runway.append(14)
                    runway14.append(runway)
                elif 300 < heading < 330:
                    runway.append(32)
                    runway14.append(runway)

                elif 150 < heading < 180:
                    runway.append(16)
                    runway16.append(runway)
                elif 330 < heading < 360:
                    runway.append(34)
                    runway16.append(runway)

                else:
                    runway.append(0)
                    wtf.append(runway)
                '''
                if realrunway == 10 or realrunway == 28:
                    runway10.append(runway)

                elif realrunway == 14 or realrunway == 32:
                    runway14.append(runway)


                elif realrunway == 16 or realrunway == 34:

                    runway16.append(runway)'''
                #runways.append(runway)
                # Dit is dus je runway + de timestamp van vertrek.

            #print(runway)

runway10fin = sort_runway_time(runway10)
runway14fin = sort_runway_time(runway14)
runway16fin = sort_runway_time(runway16)
wtffin = sort_runway_time(wtf)

print('runway10')
print(runway10fin)
print(len(runway10fin))
print('runway 14')
print(runway14)
print('runway16')
print(runway16)
print('wtf')
print(wtffin)



if "runway_usage" not in os.listdir(os.getcwd() + "\\data"):
    os.mkdir(f"data\\runway_usage")

panda_columns = ['runway', 'flight_id', 'icao24', 'timestamp', 'arriving', 'heading', 'new_runway']

runway10panda = pd.DataFrame(list(runway10fin), columns = panda_columns)
runway10panda.to_csv('data\\runway_usage\\runway10_28_new.csv', index=False)
runway14panda = pd.DataFrame(list(runway14fin), columns = panda_columns)
runway14panda.to_csv('data\\runway_usage\\runway14_32_new.csv', index=False)
runway16panda = pd.DataFrame(list(runway16fin), columns = panda_columns)
runway16panda.to_csv('data\\runway_usage\\runway16_34_new.csv', index=False)
wtfpanda = pd.DataFrame(list(wtf), columns = panda_columns)
wtfpanda.to_csv('data\\runway_usage\\wtf.csv', index=False)

all_runways = runway10panda.append(runway14panda).append(runway16panda).append(wtfpanda).sort_values(by="timestamp")

print(all_runways.loc[all_runways['runway']!=all_runways['new_runway']])