# imports
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import os

# dataframe imports
weather_oct = pd.read_csv(".\\data\\dataset_oct.txt", names = ["Day", "DayNumber", "Time", "Temp", "Weather", "WindSpeed", "WindDirection", "Humidity", "Pressure", "Visibility"])
weather_nov = pd.read_csv(".\\data\\dataset_nov.txt", names = ["Day", "DayNumber", "Time", "Temp", "Weather", "WindSpeed", "WindDirection", "Humidity", "Pressure", "Visibility"])
weather_oct["Month"] = 10
weather_nov["Month"] = 11

# merging october and november
weather = pd.concat([weather_oct, weather_nov], ignore_index = True)

# Cleaning up weather dataframe:

# Removing leftover [] and ''
weather["Day"] = weather["Day"].map(lambda x: x.lstrip('['))
weather["Visibility"] = weather["Visibility"].map(lambda x: x.rstrip(']'))
weather["Weather"] = weather["Weather"].map(lambda x: x.lstrip(" '"))
weather["Weather"] = weather["Weather"].map(lambda x: x.rstrip("'"))
weather["Visibility"] = weather["Visibility"].map(lambda x: x.lstrip(" '"))
weather["Visibility"] = weather["Visibility"].map(lambda x: x.rstrip("'"))
weather["Time"] = weather["Time"].map(lambda x: x.lstrip(" '"))
weather["Time"] = weather["Time"].map(lambda x: x.rstrip("'"))

# Remove useless (?) day entry number
if "DayNumber" in weather.columns:
    weather.drop(["DayNumber"], axis = 1, inplace = True)

# set datum in same format as ads-b data:

# turn time column into list
if isinstance(weather["Time"][0], str): #simple check if function has already been performed (for notebook)
    weather["Hour"] = weather["Time"].str.split(pat = ":").str[0]
    weather["Min"] = weather["Time"].str.split(pat = ":").str[1]

#convert to integers
weather[["Day", "Hour", "Min"]] = weather[["Day", "Hour", "Min"]].astype(int)

# make datetime column
weather['NewTime'] = pd.to_datetime({'year':2019, 'month':weather["Month"], 'day':weather['Day'], 'hour':weather['Hour'], 'minute':weather['Min']}, utc=True)


# now we don't care about the individual time columns anymore so we remove them
for i in ["Day", "Time", "Month", "Hour", "Min"]:
    if i in weather.columns:
        weather.drop(i, axis = 1, inplace = True)

# Definitions
def find_weather(data1, arrival = True):
    data1["timestamp"] = pd.to_datetime(data["timestamp"])
    if arrival:
        reftime = data1.iloc[-1]["timestamp"]
    else:
        reftime = data1.iloc[0]["timestamp"]
    timediffs = abs((weather["NewTime"]-reftime))
    return weather.iloc[timediffs.argmin()], reftime


def add_to_weather(flightweather, data2, ID, arr):
    row, time = find_weather(data2, arr)
    series = pd.Series({'flight_ID': ID,
                        'Temperature': row['Temp'],
                        'Weather': row['Weather'],
                        'WindSpeed': row['WindSpeed'],
                        'WindDirection': row['WindDirection'], 
                        'Humidity':row['Humidity'], 
                        'Pressure':row['Pressure'], 
                        'Visibility':row['Visibility'],
                        'Time':time
           })
    flightweather = flightweather.append(series, ignore_index=True)
    return flightweather


# Make empty dataframes
arrival_weather = pd.DataFrame(columns=['flight_ID', 'Temperature', 'Weather', 'WindSpeed', 'WindDirection', 'Humidity', 'Pressure', 'Visibility', 'Time'])
departure_weather = pd.DataFrame(columns=['flight_ID', 'Temperature', 'Weather', 'WindSpeed', 'WindDirection', 'Humidity', 'Pressure', 'Visibility', 'Time'])

flight_num = 100000

# ARRIVAL
arrival_list = os.listdir(os.getcwd() + '\\data\\arrival_flights')
for f in range(0, min(len(arrival_list), flight_num)):
    if not arrival_list[f].startswith('.') and not arrival_list[f][-4:] == ".csv":
        #print("\nfolder: ", arrival_list[f])
        for file in os.listdir(os.getcwd() + f'\\data\\arrival_flights\\{arrival_list[f]}'):
            if file[-4:] == ".csv":
                #print(file)
                data = pd.read_csv(f"data\\arrival_flights\\{arrival_list[f]}\\{file}")
                ID = file[:-4]
                arrival_weather = add_to_weather(arrival_weather, data, ID, arr = True)
print("Arrival: Done")

# DEPARTURE
departure_list = os.listdir(os.getcwd() + '\\data\\departure_flights')
for f in range(0, min(len(departure_list), flight_num)):
    if not departure_list[f].startswith('.') and not departure_list[f][-4:] == ".csv":
        for file in os.listdir(os.getcwd() + f'\\data\\departure_flights\\{departure_list[f]}'):
            if file[-4:] == ".csv":
                data = pd.read_csv(f"data\\departure_flights\\{departure_list[f]}\\{file}")
                ID = file[:-4]
                departure_weather = add_to_weather(departure_weather, data, ID, arr = False)
print("Departure: Done")

# Exporting
arrival_weather.to_csv("Arrival_Weather.csv", index = True)#, sep = "\t")
departure_weather.to_csv("Departure_Weather.csv", index = True)




