import pandas as pd 
import matplotlib.pyplot as plt
import sys
import os
import cartopy
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
    "physical",
    "lakes",
    "10m",
    facecolor = "b",
    alpha = 0.5
)
urban = feature.NaturalEarthFeature(
    "cultural",
    "populated_places",
    "10m"
)

def custom_plot():
    ax.add_feature(land)
    ax.add_feature(borders)
    ax.add_feature(lakes)
    ax.set_extent([7.54, 9.8, 46.73, 48.16])

def Stamen_terrain_background_plot():
    tiler = Stamen('terrain-background')
    ax.set_extent([7.54, 9.8, 46.73, 48.16])
    zoom = 10
    ax.add_image(tiler, zoom, interpolation='spline36')
    ax.add_feature(borders)
    ax.plot([8.535937,8.556704],[47.475701,47.445563],transform=cartopy.crs.Geodetic(), linewidth= 4, color = 'black')

def tryout_plot():
    tiler = Stamen('terrain')
    ax.set_extent([7.54, 9.8, 46.73, 48.16])
    zoom = 8
    ax.add_image(tiler, zoom, interpolation='spline36')
    ax.add_feature(borders)

ax = plt.subplot(111, projection=cartopy.crs.Mercator())
#custom_plot()
Stamen_terrain_background_plot()
#tryout_plot()


def plot_arrival_track(lon, lat):
    ax.plot(lon, lat, transform=cartopy.crs.Geodetic(), color= "b", linewidth=0.4)

def plot_departure_track(lon,lat):
    ax.plot(lon, lat, transform=cartopy.crs.Geodetic(), color= "r", linewidth=0.4)


def all_arrival_flights():
    for folder in os.listdir(os.getcwd() + f'\\data\\arrival_flights'):
        if os.path.isdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
            for file in os.listdir(os.getcwd() + f"\\data\\arrival_flights\\{folder}"):
                if file[-4:] == ".csv":
                    arrival_file = pd.read_csv(f"data\\arrival_flights\\{folder}\\{file}").values
                    lat,lon = arrival_file[:,7],arrival_file[:,8]
                    plot_arrival_track(lon, lat)
    

def all_departure_flights():    
    for folder in os.listdir(os.getcwd() + f'\\data\\departure_flights'):
        if os.path.isdir(os.getcwd() + f"\\data\\departure_flights\\{folder}"):
            for file in os.listdir(os.getcwd() + f"\\data\\departure_flights\\{folder}"):
                if file[-4:] == ".csv":
                    departure_file = pd.read_csv(f"data\\departure_flights\\{folder}\\{file}").values
                    lat,lon = departure_file[:,8],departure_file[:,9]
                    plot_departure_track(lon, lat)
    

def part_of_arrival_flights():
    flight_num = 10

    arrival_list = os.listdir(os.getcwd() + '\\data\\arrival_flights')

    for f in range(0, min(len(arrival_list), flight_num)):
        print(arrival_list[f])
        if os.path.isdir(os.getcwd() + f"\\data\\arrival_flights\\{arrival_list[f]}"):
            for file in os.listdir(os.getcwd() + f"\\data\\arrival_flights\\{arrival_list[f]}"):
                if file[-4:] == ".csv":
                    arrival_file = pd.read_csv(f"data\\arrival_flights\\{arrival_list[f]}\\{file}").values
                    lat,lon = arrival_file[:,7],arrival_file[:,8]
                    plot_arrival_track(lon, lat)    

def part_of_departure_flights():
    flight_num = 10

    departure_list = os.listdir(os.getcwd() + '\\data\\departure_flights')

    for f in range(0, min(len(departure_list), flight_num)):
        print(departure_list[f])
        if os.path.isdir(os.getcwd() + f"\\data\\departure_flights\\{departure_list[f]}"):
            for file in os.listdir(os.getcwd() + f"\\data\\departure_flights\\{departure_list[f]}"):
                if file[-4:] == ".csv":
                    departure_file = pd.read_csv(f"data\\departure_flights\\{departure_list[f]}\\{file}").values
                    lat,lon = departure_file[:,8],departure_file[:,9]
                    plot_departure_track(lon, lat)    
    
def specific_runway_flights(runwayfile, direction):
    runway_file = os.path.join(os.getcwd() + runwayfile)
    runway_values = pd.read_csv(runway_file).values
    flight_id_list = list(runway_values[:,1])
    if direction.lower()[0]=="a": direction_folder,direction_check = os.path.join(os.getcwd() + f'\\data\\arrival_flights'), True
    else: direction_folder,direction_check = os.path.join(os.getcwd() + f'\\data\\departure_flights'), False

    for folder in os.listdir(direction_folder):
        if os.path.isdir(direction_folder + f"\\{folder}"):
            for file in os.listdir(direction_folder +  f"\\{folder}"):
                if file[:-4] in flight_id_list:
                    arriving = runway_values[flight_id_list.index(file[:-4]),4]
                    if (arriving and direction_check) or (arriving==False and direction_check==False):
                        if file[-4:] == ".csv":
                            flight_file = pd.read_csv(os.path.join(direction_folder + f"\\{folder}\\{file}")).values
                            if direction_check:
                                lat,lon = flight_file[:,7],flight_file[:,8]
                                plot_arrival_track(lon, lat)
                            else: 
                                lat,lon = flight_file[:,8],flight_file[:,9]
                                plot_departure_track(lon, lat)


#part_of_arrival_flights()
#part_of_departure_flights()

#specific_runway_flights("\\data\\runway16_34.csv" , "arrival" )
specific_runway_flights("\\data\\runway16_34.csv" , "departure" )
#all_arrival_flights()
#all_departure_flights()

#plt.savefig("file.png",bbox = "tight",dpi = 3600)
# or (arriving==False and direction.lower()[0]=="d")

plt.show()