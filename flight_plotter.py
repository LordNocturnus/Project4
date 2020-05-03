import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines
import sys
import os
import time
import math
import cartopy
from textwrap import wrap
from datetime import datetime
from scipy import optimize
from cartopy import feature
from cartopy.io.img_tiles import Stamen

land = feature.NaturalEarthFeature(
    "physical", "land", "10m", edgecolor="gray", facecolor="#dddddd", linewidth=0.5
)
borders = feature.NaturalEarthFeature(
    "cultural",
    "admin_0_boundary_lines_land",
    "10m",
    edgecolor="black",
    facecolor="none",
    linestyle=":",
)
lakes = feature.NaturalEarthFeature(
    "physical", "lakes", "10m", facecolor="b", alpha=0.5
)
urban = feature.NaturalEarthFeature("cultural", "populated_places", "10m")


def custom_plot(ax):
    ax.add_feature(land)
    ax.add_feature(borders)
    ax.add_feature(lakes)
    ax.set_extent([7.54, 9.8, 46.73, 48.16])


def Stamen_terrain_background_plot(ax):
    tiler = Stamen("terrain-background")
    ax.set_extent([7.346245, 9.75, 46.65119, 48.27896])
    zoom = 10
    ax.add_image(tiler, zoom, interpolation="spline36")
    ax.add_feature(borders)


def plot_runway(ax,runways):
    # outputs the runways you want
    # runways = [10,14,16] or [28,32,34]
    def runway16_34(ax,lw):
        ax.plot(
        [8.535937, 8.556704],
        [47.475701, 47.445563],
        transform=cartopy.crs.Geodetic(),
        linewidth=lw,
        color="black")
    def runway14_32(ax,lw):
        ax.plot(
            [8.536075, 8.564459],
            [47.482093, 47.461292],
            transform=cartopy.crs.Geodetic(),
            linewidth=lw,
            color="black")
    def runway10_28(ax,lw):
        ax.plot(
            [8.537482, 8.570386],
            [47.458947, 47.456602],
            transform=cartopy.crs.Geodetic(),
            linewidth=lw,
            color="black")
    
    def which_runway(runway,lw):
        if runway==(16 or 34): runway16_34(ax,lw)
        if runway==(14 or 32): runway14_32(ax,lw)
        if runway==(10 or 28): runway10_28(ax,lw)

    if len(runways)==1:
        runway = runways[0]
        which_runway(runway,4)
    else:
        for runway in runways:
            which_runway(runway,2)


def plot_arrival_track(ax,lon,lat,alpha_value):
    ax.plot(lon, lat, transform=cartopy.crs.Geodetic(), color="b", linewidth=0.4, alpha=alpha_value)


def plot_departure_track(ax, lon, lat,alpha_value):
    ax.plot(lon, lat, transform=cartopy.crs.Geodetic(), color="r", linewidth=0.4, alpha=alpha_value)


def transparency(number_of_flights):
    if number_of_flights<998:
        return -math.log(number_of_flights/600+1, math.exp(1))+1
    else: return 0.02


def part_of_flights(start,end,subplot_number):
    start_time = time.time()
    ax = plt.subplot(subplot_number, projection=Stamen('terrain-background').crs)
    Stamen_terrain_background_plot(ax)
    plot_runway(ax,[10,14,16])
    icao_data = pd.read_csv(os.path.join(os.getcwd()+"\\data\\icao24.csv"))
    icao_data = icao_data.sort_values("timestamp")
    start_date = datetime.strptime(start,"%Y-%m-%d %H:%M:%S+00:00")
    end_date = datetime.strptime(end,"%Y-%m-%d %H:%M:%S+00:00")
    icao_data["timestamp"] = [datetime.strptime(date,"%Y-%m-%d %H:%M:%S+00:00") for date in pd.array(icao_data["timestamp"])]
    condition = (icao_data["timestamp"]>= start_date) & (icao_data["timestamp"] <= end_date)
    part_of_dataframe = icao_data[condition]
    #Now we have the desired part of the dataframe
    flight_id_list = list(part_of_dataframe["flight_id"])
    flights = [os.path.join(os.getcwd() + f"\\data\\arrival_flights"),
             os.path.join(os.getcwd() + f"\\data\\departure_flights")]
    N_of_flights = 0
    for item in flights:
        for folder in os.listdir(item):
            if os.path.isdir(item + f"\\{folder}"):
                for file in os.listdir(item + f"\\{folder}"):
                    if file[:-4] in flight_id_list:
                        N_of_flights+=1
    alpha_value = transparency(N_of_flights)

    for item in flights:
        for folder in os.listdir(item):
            if os.path.isdir(item + f"\\{folder}"):
                for file in os.listdir(item + f"\\{folder}"):
                    if file[:-4] in flight_id_list:
                        index = flight_id_list.index(file[:-4])
                        arriving = pd.array(part_of_dataframe["arriving"])[index]
                    
                        flight_file = pd.read_csv(
                            os.path.join(item + f"\\{folder}\\{file}")
                        ).values
                        
                        if arriving:
                            lat, lon = flight_file[:, 7], flight_file[:, 8]
                            plot_arrival_track(ax, lon, lat,alpha_value)
                        else:
                            lat, lon = flight_file[:, 8], flight_file[:, 9]
                            plot_departure_track(ax, lon, lat,alpha_value)
    
    plt.legend(handles=[matplotlib.lines.Line2D([0], [0], color='b', lw=4, label='Arriving'),
        matplotlib.lines.Line2D([0], [0], color='r', lw=4, label='Departing')],loc="upper right")
    title = ax.set_title("\n".join(wrap(f'Flight trajectories between {start_date} and {end_date}', 50)))
    title.set_y(1.05)    
    print(time.time()-start_time)

    
def all_arrival_flights():
    start_time = time.time()
    N_flights = 19480
    ax = plt.subplot(111, projection=Stamen('terrain-background').crs)
    Stamen_terrain_background_plot(ax)
    for folder in os.listdir(os.getcwd() + f"\\data\\arrival_flights"):
        if os.path.isdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
            for file in os.listdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
                if file[-4:] == ".csv":
                    arrival_file = pd.read_csv(
                        f"data\\arrival_flights\\{folder}\\{file}"
                    ).values
                    lat, lon = arrival_file[:, 7], arrival_file[:, 8]
                    plot_arrival_track(ax,lon,lat,0.02)
    
    print(time.time()-start_time)


def all_departure_flights():
    for folder in os.listdir(os.getcwd() + f"\\data\\departure_flights"):
        if os.path.isdir(os.getcwd() + f"\\data\\departure_flights\\{folder}"):
            for file in os.listdir(
                os.getcwd() + f"\\data\\departure_flights\\{folder}"
            ):
                if file[-4:] == ".csv":
                    departure_file = pd.read_csv(
                        f"data\\departure_flights\\{folder}\\{file}"
                    ).values
                    lat, lon = departure_file[:, 8], departure_file[:, 9]
                    plot_departure_track(ax, lon, lat,0.02)


def first_N_arrival_flights():
    flight_num = 1000
    ax = plt.subplot(111, projection=Stamen('terrain-background').crs)
    Stamen_terrain_background_plot(ax)
    plot_runway(ax,[10,14,16])
    alpha_value = transparency(flight_num)
    print(alpha_value)
    arrival_list = os.listdir(os.getcwd() + "\\data\\arrival_flights")

    for f in range(0, min(len(arrival_list), flight_num)):
        if os.path.isdir(os.getcwd() + f"\\data\\arrival_flights\\{arrival_list[f]}"):
            for file in os.listdir(
                os.getcwd() + f"\\data\\arrival_flights\\{arrival_list[f]}"
            ):
                if file[-4:] == ".csv":
                    arrival_file = pd.read_csv(
                        f"data\\arrival_flights\\{arrival_list[f]}\\{file}"
                    ).values
                    lat, lon = arrival_file[:, 7], arrival_file[:, 8]
                    plot_arrival_track(ax,lon,lat,alpha_value)


def first_N_departure_flights():
    flight_num = 10

    departure_list = os.listdir(os.getcwd() + "\\data\\departure_flights")

    for f in range(0, min(len(departure_list), flight_num)):
        print(departure_list[f])
        if os.path.isdir(
            os.getcwd() + f"\\data\\departure_flights\\{departure_list[f]}"
        ):
            for file in os.listdir(
                os.getcwd() + f"\\data\\departure_flights\\{departure_list[f]}"
            ):
                if file[-4:] == ".csv":
                    departure_file = pd.read_csv(
                        f"data\\departure_flights\\{departure_list[f]}\\{file}"
                    ).values
                    lat, lon = departure_file[:, 8], departure_file[:, 9]
                    plot_departure_track(ax, lon, lat,1)


def specific_runway_flights(number_1, number_2, runwayfile, direction):
    runway_file = os.path.join(os.getcwd() + runwayfile)
    runway_values = pd.read_csv(runway_file).values
    flight_id_list = list(runway_values[:, 1])
    ax1 = plt.subplot(121, projection=cartopy.crs.Mercator())
    Stamen_terrain_background_plot(ax1)
    ax2 = plt.subplot(122, projection=cartopy.crs.Mercator())
    Stamen_terrain_background_plot(ax2)
    runways = [number_1]
    plot_runway(ax1,runways)
    plot_runway(ax2,runways)
    if direction.lower()[0] == "a":
        direction_folder, direction_check = (
            os.path.join(os.getcwd() + f"\\data\\arrival_flights"),
            True,
        )
        ax1.legend(handles = [matplotlib.lines.Line2D([0], [0], color='b', lw=4, label='Arriving'),
            matplotlib.lines.Line2D([0], [0], color='black', lw=6, label=f'Runway {number_1}')], loc="upper right")
        ax2.legend(handles = [matplotlib.lines.Line2D([0], [0], color='b', lw=4, label='Arriving'),
            matplotlib.lines.Line2D([0], [0], color='black', lw=6, label=f'Runway {number_2}')],loc="upper right")   
    else:
        direction_folder, direction_check = (
            os.path.join(os.getcwd() + f"\\data\\departure_flights"),
            False,
        )
        ax1.legend(handles = [matplotlib.lines.Line2D([0], [0], color='r', lw=4, label='Departing'),
            matplotlib.lines.Line2D([0], [0], color='black', lw=6, label=f'Runway {number_1}')],loc="upper right")
        ax2.legend(handles = [matplotlib.lines.Line2D([0], [0], color='r', lw=4, label='Departing'),
            matplotlib.lines.Line2D([0], [0], color='black', lw=6, label=f'Runway {number_2}')],loc="upper right")

    for folder in os.listdir(direction_folder):
        if os.path.isdir(direction_folder + f"\\{folder}"):
            for file in os.listdir(direction_folder + f"\\{folder}"):
                if file[:-4] in flight_id_list:
                    index = flight_id_list.index(file[:-4])
                    arriving = runway_values[index, 4]
                    if (arriving and direction_check) or (
                        arriving == False and direction_check == False
                    ):
                        if file[-4:] == ".csv":
                            flight_file = pd.read_csv(
                                os.path.join(direction_folder + f"\\{folder}\\{file}")
                            ).values
                            if runway_values[index, 0] == number_1:
                                if direction_check:
                                    lat, lon = flight_file[:, 7], flight_file[:, 8]
                                    plot_arrival_track(ax1, lon, lat,0.02)
                                else:
                                    lat, lon = flight_file[:, 8], flight_file[:, 9]
                                    plot_departure_track(ax1, lon, lat,0.02)
                            if runway_values[index, 0] == number_2:
                                if direction_check:
                                    lat, lon = flight_file[:, 7], flight_file[:, 8]
                                    plot_arrival_track(ax2, lon, lat,0.02)
                                else:
                                    lat, lon = flight_file[:, 8], flight_file[:, 9]
                                    plot_departure_track(ax2, lon, lat,0.02)

def specific_runway_arrival_and_departure(number_1, number_2, runwayfile):
    runway_file = os.path.join(os.getcwd() + runwayfile)
    runway_values = pd.read_csv(runway_file).values
    flight_id_list = list(runway_values[:, 1])
    ax1 = plt.subplot(121, projection=cartopy.crs.Mercator())
    Stamen_terrain_background_plot(ax1)
    ax2 = plt.subplot(122, projection=cartopy.crs.Mercator())
    Stamen_terrain_background_plot(ax2)
    ax1.legend(handles = [matplotlib.lines.Line2D([0], [0], color='b', lw=4, label='Arriving'),
        matplotlib.lines.Line2D([0], [0], color='r', lw=4, label='Departing'),
        matplotlib.lines.Line2D([0], [0], color='black', lw=6, label= f'Runway {number_1}')],loc="upper right")
    ax2.legend(handles = [matplotlib.lines.Line2D([0], [0], color='b', lw=4, label='Arriving'),
        matplotlib.lines.Line2D([0], [0], color='r', lw=4, label='Departing'),
        matplotlib.lines.Line2D([0], [0], color='black', lw=6, label=f'Runway {number_2}')],loc="upper right")   
    runways = [number_1]
    plot_runway(ax1,runways)
    plot_runway(ax2,runways)
    runway_flights = [[10,22],[28,16484],[14,14494],[32,3569],[16,2423],[34,1996]] #precomputed number of flights per runway
    runway_flights = pd.DataFrame(runway_flights, columns = ["runway","N"])
    number_of_flights_1 = runway_flights[runway_flights["runway"]==number_1]["N"].values[0]
    number_of_flights_2 = runway_flights[runway_flights["runway"]==number_2]["N"].values[0]
    alpha_value_1 = transparency(number_of_flights_1)
    alpha_value_2 = transparency(number_of_flights_2)
    flights = [os.path.join(os.getcwd() + f"\\data\\arrival_flights"),
             os.path.join(os.getcwd() + f"\\data\\departure_flights")]
        
    for item in flights:
        for folder in os.listdir(item):
            if os.path.isdir(item + f"\\{folder}"):
                for file in os.listdir(item + f"\\{folder}"):
                    if file[:-4] in flight_id_list:
                        index = flight_id_list.index(file[:-4])
                        arriving = runway_values[index, 4]
                        if file[-4:] == ".csv":
                            flight_file = pd.read_csv(
                                os.path.join(item + f"\\{folder}\\{file}")
                            ).values
                            if runway_values[index, 0] == number_1:
                                if arriving:
                                    lat, lon = flight_file[:, 7], flight_file[:, 8]
                                    plot_arrival_track(ax1, lon, lat,alpha_value_1)
                                else:
                                    lat, lon = flight_file[:, 8], flight_file[:, 9]
                                    plot_departure_track(ax1, lon, lat,alpha_value_1)
                            if runway_values[index, 0] == number_2:
                                if arriving:
                                    lat, lon = flight_file[:, 7], flight_file[:, 8]
                                    plot_arrival_track(ax2, lon, lat,alpha_value_2)
                                else:
                                    lat, lon = flight_file[:, 8], flight_file[:, 9]
                                    plot_departure_track(ax2, lon, lat,alpha_value_2)
    

#plt.figure(figsize=(16,9))

#all_arrival_flights()
#first_N_arrival_flights()
#specific_runway_flights(14, 32, "\\data\\runway14_32.csv", "arrival")
#specific_runway_arrival_and_departure(10,28,"\\data\\runway10_28.csv")
#part_of_flights("2019-10-01 04:01:12+00:00","2019-11-30 22:13:46+00:00",111)
#part_of_flights("2019-11-14 10:55:15+00:00","2019-11-15 12:26:40+00:00",111)
#part_of_flights("2019-11-09 21:30:00+00:00","2019-11-10 07:00:00+00:00",111)
#plt.savefig("file.pdf",bbox = "tight")
#plt.show()

#Helper functions

def filesaver():
    filesaving = [(10,28),(14,32),(16,34)]

    for i in range(len(filesaving)):
        number1,number2 = filesaving[i][0],filesaving[i][1]
        specific_runway_flights(number1, number2, f"\\data\\runway{number1}_{number2}.csv", "arrival")
        plt.savefig(f"spec_runway_{number1}_{number2}_arrival.png",bbox = "tight",dpi = 500)
        plt.clf() 
        specific_runway_flights(number1, number2, f"\\data\\runway{number1}_{number2}.csv", "departure")
        plt.savefig(f"spec_runway_{number1}_{number2}_departure.png",bbox = "tight",dpi = 500)
        plt.clf()
        specific_runway_arrival_and_departure(number1,number2,f"\\data\\runway{number1}_{number2}.csv")
        plt.savefig(f"spec_runway_{number1}_{number2}_arr_and_dep.png",bbox = "tight",dpi = 500)
        plt.clf()

#filesaver()

def check_runway_entries():
    runway_values = pd.read_csv(os.path.join(os.getcwd() + "\\data\\runway14_32.csv")).values
    i=0
    k=0
    for j in range(len(runway_values)): 
        if runway_values[j,0]==14 and runway_values[j,4]==True:
            i+=1
        if runway_values[j,0]==32 and runway_values[j,4]==True:
            k+=1
    print(f"i is {i}")
    print(f"k is {k}")
        
#8.530562783707047 47.471626608073855 0.9014288817329612 (circle of the adsb data)
# scale factor is 1.4793879