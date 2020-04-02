import sys
import pandas as pd
import matplotlib.pyplot as plt
import cartopy
import bootstrap
from scipy import signal


df_adsb = pd.read_csv("data/kl1793_adsb.csv")
df_adsb["alt"] = df_adsb["baroaltitude"] * 3.28084
df_adsb["spd"] = df_adsb["velocity"] * 1.94384
t0 = df_adsb["time"].min()
df_adsb["time"] = df_adsb["time"] - t0
df_ehs = pd.read_csv("data/kl1793_ehs.csv")
df_ehs["time"] = df_ehs["time"] - t0

df_adsb = df_adsb[df_adsb.time < df_ehs.time.max()]
df_adsb = df_adsb[df_adsb.time > df_ehs.time.min()]


@bootstrap.handlefig
def plot_track(*args, **kwargs):
    bootstrap.fig7()

    lon, lat = (
        df_adsb.dropna(subset=["lon"]).lon.values,
        df_adsb.dropna(subset=["lat"]).lat.values,
    )
    ax1 = plt.subplot(111, projection=cartopy.crs.EuroPP())
    ax1.add_feature(bootstrap.land)
    ax1.add_feature(bootstrap.borders)
    ax1.plot(lon, lat, transform=cartopy.crs.Geodetic(), color="k")
    ax1.text(lon[0] - 1, lat[0] + 0.2, "EHAM", transform=cartopy.crs.Geodetic())
    ax1.text(lon[-1] + 0.5, lat[-1], "EDDM", transform=cartopy.crs.Geodetic())
    ax1.set_extent([-2, 17, 46, 55])

    return plt


@bootstrap.handlefig
def plot_alt(*args, **kwargs):
    bootstrap.fig7()

    ax1 = plt.subplot(111)

    ax1.scatter(
        df_ehs.dropna(subset=["selalt40mcp"]).time,
        signal.medfilt(
            df_ehs.dropna(subset=["selalt40mcp"]).selalt40mcp / 1000, kernel_size=11
        ),
        color=bootstrap.red,
        s=15,
        label="selected altitude (EHS)",
    )

    ax1.plot(
        df_adsb.dropna(subset=["alt"]).time,
        signal.medfilt(df_adsb.dropna(subset=["alt"]).alt / 1000, kernel_size=11),
        color="k",
        label="altitude",
    )
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Altitude (kft)")
    plt.ylim([0, 32])
    plt.legend()
    plt.grid()

    return plt


@bootstrap.handlefig
def plot_speed(*args, **kwargs):
    bootstrap.fig7()
    ax1 = plt.subplot(111)
    ax1.plot(
        df_ehs.dropna(subset=["gs50"]).time,
        signal.medfilt(df_ehs.dropna(subset=["gs50"]).gs50, kernel_size=11),
        label="ground speed (EHS)",
        color=bootstrap.red,
        lw=3,
    )
    ax1.plot(
        df_adsb.dropna(subset=["spd"]).time,
        signal.medfilt(df_adsb.dropna(subset=["spd"]).spd, kernel_size=11),
        color="k",
        label="ground speed (ADS-B)",
    )
    ax1.plot(
        df_ehs.dropna(subset=["tas50"]).time,
        signal.medfilt(df_ehs.dropna(subset=["tas50"]).tas50, kernel_size=11),
        label="true airspeed (EHS)",
        color=bootstrap.green,
    )
    ax1.plot(
        df_ehs.dropna(subset=["ias60"]).time,
        signal.medfilt(df_ehs.dropna(subset=["ias60"]).ias60, kernel_size=11),
        label="indicated airspeed (EHS)",
        color=bootstrap.blue,
    )
    ax1.plot(
        [1000, 1000], [200, 200], color="purple", ls=":", label="mach number (EHS)"
    )  # just for ploting the label for mach
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Speed (kt)")
    ax1.set_ylim([50, 500])
    plt.grid()
    plt.legend()

    ax2 = ax1.twinx()
    ax2.plot(
        df_ehs.dropna(subset=["mach60"]).time,
        signal.medfilt(df_ehs.dropna(subset=["mach60"]).mach60, kernel_size=11),
        color="purple",
        ls=":",
    )
    ax2.set_ylabel("Mach (-)")
    ax2.set_ylim([0.1, 1])

    return plt


if __name__ == "__main__":

    save = sys.argv[1] if len(sys.argv) > 1 else False
    plot_track(save=save, name="example_flight_track")
    plot_alt(save=save, name="example_flight_alt")
    plot_speed(save=save, name="example_flight_speed")
