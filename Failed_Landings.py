import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import numpy as np

failed_landings = np.empty(0)

for folder in os.listdir(os.getcwd() + f"\\data\\arrival_flights"):
    if os.path.isdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
        for file in os.listdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
            if file[-4:] == ".csv":
                arrival_file = pd.read_csv(f"data\\arrival_flights\\{folder}\\{file}").values

                geoalt = arrival_file[:, 3]
                alt = arrival_file[:,1]



                for i in range(len(geoalt)):
                    if arrival_file[0,-2] == 'YUPZM_19073':
                        print('done')
                        quit()

                    elif geoalt[i] <= 2200 and geoalt[i] != geoalt[-1] : # to check if it is close to landing but not landed yet
                        #if geoalt[i + 1] <= geoalt[i] :  # check if it is still descending or level
                            #okay
                            #print('Descending')
                        if geoalt[i] > geoalt[i-1] and geoalt[i] != geoalt[-1]:
                            if geoalt[i + 1] > geoalt[i] and geoalt[i + 1] != geoalt[-1] and geoalt[i + 2] > geoalt[i + 1] and geoalt[i + 2] != geoalt[-1]:
                                print('failed landing attempt')
                                print(arrival_file[0,-2])
                                print(arrival_file[0,2])
                                print(arrival_file[i+3,0])
                                #if 'arrival_file[0.2]' not in failed_landings:
                                #if arrival_file[i,:] not in failed_landings:
                                failed_landings.np.append(arrival_file[i,:])

                        elif geoalt[i + 1] == geoalt[-1]:
                            break

print(failed_landings)
#def Zurich_Altitude_check
    #Geo_Altitude_zurich = roughly 1417 feet
    #Range of minimum geoaltitudes recorded at landing: 1850 -- 1450 'feet'
