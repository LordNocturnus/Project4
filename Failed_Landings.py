import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import numpy as np

failed_landings = []
failed_landings_Codes = []

for folder in os.listdir(os.getcwd() + f"\\data\\arrival_flights"):
    if os.path.isdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
        for file in os.listdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
            if file[-4:] == ".csv":
                arrival_file = pd.read_csv(f"data\\arrival_flights\\{folder}\\{file}").values

                geoalt = arrival_file[:, 3]
                alt = arrival_file[:,1]



                for i in range(len(geoalt)):
                    if arrival_file[0,-2] == 'YUPZM_19073':
                        print(failed_landings)
                        failed_landings_Codes = list(dict.fromkeys(failed_landings_Codes))
                        print(failed_landings_Codes)
                        print('done')
                        quit()

                    elif geoalt[i-1] <= 3000 and arrival_file[i-1,0] != arrival_file[-1,0] : # to check if it is close to landing but not landed yet
                        #if geoalt[i + 1] <= geoalt[i] :  # check if it is still descending or level
                            #okay
                            #print('Descending')
                        if geoalt[i] > geoalt[i-1] and arrival_file[i,0] != arrival_file[-1,0]:
                            if geoalt[i + 1] > geoalt[i] and arrival_file[i+1,0] != arrival_file[-1,0]:
                                #print('failed landing attempt')
                                #print(arrival_file[0,-2])
                                #print(arrival_file[0,2])
                                #print(arrival_file[i+3,0])
                                #if 'arrival_file[0.2]' not in failed_landings:
                                #if arrival_file[i,:] not in failed_landings:
                                failed_landings.append(arrival_file[i,:])
                                failed_landings_Codes.append(arrival_file[0,-2])


                        elif geoalt[i] == geoalt[-1] and arrival_file[i,0] == arrival_file[-1,0]:
                            break


#def Zurich_Altitude_check
#Geo_Altitude_zurich = roughly 1417 feet
#Range of minimum geoaltitudes recorded at landing: 1850 -- 1450 'feet'

