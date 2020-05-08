#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:57:13 2020

@author: MatthiasChristiaens
"""
# imports
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

# add your flight IDs to this list and it will plot them
idlist = ["2KYCM_3248"]

# keep empty
loclist = []

# get path
for i in idlist:
    k = i.split("_")[0]
    loc = "./data/arrival_flights/"+k+"/"+i+".csv"
    loclist.append(loc)

#print(idlist[0])
    
# Plot nth entry in list
number = 0
data = pd.read_csv(loclist[number]) #you can also just directly input the path

fig = plt.figure()
ax = fig.gca(projection='3d')
plt.title(idlist[number])
ax.scatter(data['longitude'], data['latitude'], data["geoaltitude"], s = 6)

