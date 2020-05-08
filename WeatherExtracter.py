import pandas as pd

arrflights = pd.read_csv("data\\Arrival_Weather.csv")
depflights = pd.read_csv("data\\Departure_Weather.csv")


lst = []

for i, flight in arrflights.iterrows():
    date = flight['Time']#[0:10]
    #time = flight['Time'][11:19]
    winddirection = flight['WindDirection']
    WindSpeed = flight['speed']
    lst.append([date, winddirection, WindSpeed])

for j, flight in depflights.iterrows():
    date = flight['Time']#[0:10]
    #time = flight['Time'][11:19]
    winddirection = flight['WindDirection']
    WindSpeed = flight['speed']
    lst.append([date, winddirection, WindSpeed])

columns = ['timestamp', 'direction', 'speed']
x = pd.DataFrame(lst, columns=columns).sort_values(by=['timestamp'])

x.to_csv("data\\weatherdata.csv")