import pandas as pd 
import matplotlib.pyplot as plt
import sys
import os
import cartopy
from cartopy import feature

arrival_data = pd.read_csv(r'D:\Aerospace Engineering\2019-2020 Bsc2\Test Analysis and Simulation\AAL92_20575.csv').values
departure_data = pd.read_csv(r'D:\Aerospace Engineering\2019-2020 Bsc2\Test Analysis and Simulation\AAL93_19399.csv').values
arrival_latitude,arrival_longitude = arrival_data[:,7],arrival_data[:,8]
departure_latitude,departure_longitude = departure_data[:,8],departure_data[:,9]


print(arrival_latitude)
def generate_graph(filename,xs, ys, labels, linelabels):
    plt.plot(xs[0],ys[0], label=linelabels[0],linewidth=2,color='b')
    plt.plot(xs[1],ys[1], label=linelabels[1],linewidth=2,color='r')
    plt.plot([8.535937,8.556704],[47.475701,47.445563], label="ZRH", linewidth= 4, color = 'black')
    plt.xlabel(labels[0],fontsize="16")
    plt.ylabel(labels[1],fontsize="16")
    plt.grid(axis='both')
    plt.tick_params(axis='both', labelsize="large")
    plt.legend()
    plt.savefig(filename+".pdf",bbox_inches="tight")
    plt.show()
    plt.close()

generate_graph('test_flights',[arrival_longitude,departure_longitude],[arrival_latitude,departure_latitude],["Longitude","Latitude"],["Arriving","Departing"])

# plt.style.use('grayscale')




land = feature.NaturalEarthFeature(
    "physical", "land", "10m", edgecolor="gray", facecolor="#dddddd", linewidth=0.5
)

borders = feature.NaturalEarthFeature(
    "cultural",
    "admin_0_boundary_lines_land",
    "50m",
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

def plot_track(lon, lat):
    ax = plt.subplot(111, projection=cartopy.crs.EuroPP())
    ax.add_feature(land)
    ax.add_feature(borders)
    ax.add_feature(lakes)
    #ax.add_feature(urban)
    ax.plot(lon, lat, transform=cartopy.crs.Geodetic(), color= "b")
    ax.set_extent([6, 10, 45.8, 47.8])
    return plt

fig = plt.figure(figsize = (7, 4.326))

plot_track(arrival_longitude,arrival_latitude)
plot_track(departure_longitude, departure_latitude)
plt.show()


#df_adsb = pd.read_csv("data/kl1793_adsb.csv")
#df_adsb["alt"] = df_adsb["baroaltitude"] * 3.28084
#df_adsb["spd"] = df_adsb["velocity"] * 1.94384
#t0 = df_adsb["time"].min()
#df_adsb["time"] = df_adsb["time"] - t0
#df_ehs = pd.read_csv("data/kl1793_ehs.csv")
#df_ehs["time"] = df_ehs["time"] - t0

#df_adsb = df_adsb[df_adsb.time < df_ehs.time.max()]
#df_adsb = df_adsb[df_adsb.time > df_ehs.time.min()]


#def plot_track(*args, **kwargs):
#    matplotlib.rc("figure", figsize=(7, 4.326))
#
#    lon, lat = (
#        df_adsb.dropna(subset=["lon"]).lon.values,
#        df_adsb.dropna(subset=["lat"]).lat.values,
#    )
#    ax1 = plt.subplot(111, projection=cartopy.crs.EuroPP())
#    ax1.add_feature(bootstrap.land)
#    ax1.add_feature(bootstrap.borders)
#    ax1.plot(lon, lat, transform=cartopy.crs.Geodetic(), color="k")
#    ax1.text(lon[0] - 1, lat[0] + 0.2, "EHAM", transform=cartopy.crs.Geodetic())
#    ax1.text(lon[-1] + 0.5, lat[-1], "EDDM", transform=cartopy.crs.Geodetic())
#    ax1.set_extent([-2, 17, 46, 55])
#
#    return plt
#save = sys.argv[1] if len(sys.argv) > 1 else False
#plot_track(save=save, name="example_flight_track")

#def main():
#
#    ax = plt.axes(projection=cartopy.crs.PlateCarree())
#
#    ax.add_feature(cartopy.feature.LAND)
#    ax.add_feature(cartopy.feature.OCEAN)
#    ax.add_feature(cartopy.feature.COASTLINE)
#    ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
#    ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
#    ax.add_feature(cartopy.feature.RIVERS)
#
#    ax.set_extent([-20, 60, -40, 40])
#
#    plt.show()
#
#
#if __name__ == '__main__':
#    main()