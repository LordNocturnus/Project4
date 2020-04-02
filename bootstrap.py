import os
import matplotlib as mpl
import matplotlib.pyplot as plt

# plt.style.use('grayscale')

blue = "#1f77b4"
orange = "#ff7f0e"
green = "#2ca02c"
red = "#d62728"
purple = "#e377c2"


from cartopy import feature

land = feature.NaturalEarthFeature(
    "physical", "land", "50m", edgecolor="gray", facecolor="#dddddd", linewidth=0.5
)
borders = feature.NaturalEarthFeature(
    "cultural",
    "admin_0_boundary_lines_land",
    "50m",
    edgecolor="gray",
    facecolor="none",
    linestyle=":",
)


def fig10():
    mpl.rc("figure", figsize=(10, 6.181))


def fig8():
    mpl.rc("figure", figsize=(8, 4.944))


def fig7():
    mpl.rc("figure", figsize=(7, 4.326))


mpl.rc("font", size=12)
mpl.rc("axes", labelpad=5, linewidth=1)
mpl.rc("font", family="Charter, Utopia, serif")
mpl.rc("lines", linewidth=2, markersize=8)
mpl.rc("grid", color="lightgray")
mpl.rc("legend", markerscale=0.9, columnspacing=0.5)
mpl.rc("savefig", bbox="tight")
plt.rc("axes", axisbelow=True)

paper_root = os.path.dirname(os.path.realpath(__file__)) + "/../"


def handlefig(func):
    def wrapper_handlefig(*args, **kwargs):
        plot = func(*args, **kwargs)

        tight = kwargs.get("tight", True)
        save = kwargs.get("save", False)
        name = kwargs.get("name", None)

        if tight:
            plot.tight_layout()

        if save:
            plot.savefig(paper_root + "figures/%s.pdf" % name, bbox_inches="tight")
            plot.close()
        else:
            plt.show()

    return wrapper_handlefig
