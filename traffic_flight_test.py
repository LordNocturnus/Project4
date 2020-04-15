from traffic.data.samples import airbus_tree
from traffic.data.samples import quickstart
from traffic.data.samples import belevingsvlucht

import matplotlib.pyplot as plt

from traffic.core.projection import Amersfoort, GaussKruger, Lambert93, EuroPP
from traffic.drawing import countries

with plt.style.context("traffic"):
    fig = plt.figure()

    # Choose the projection type
    ax0 = fig.add_subplot(221, projection=EuroPP())
    ax1 = fig.add_subplot(222, projection=Lambert93())
    ax2 = fig.add_subplot(223, projection=Amersfoort())
    ax3 = fig.add_subplot(224, projection=GaussKruger())

    for ax in [ax0, ax1, ax2, ax3]:
        ax.add_feature(countries())
        # Maximum extent for the map
        ax.set_global()
        # Remove border and set transparency for background
        ax.outline_patch.set_visible(False)
        ax.background_patch.set_visible(False)

    # Flight.plot returns the result from Matplotlib as is
    # Here we catch it to reuse the color of each trajectory
    ret, *_ = quickstart["AFR27GH"].plot(ax0)
    quickstart["AFR27GH"].plot(
        ax1, color=ret.get_color(), linewidth=2
    )

    ret, *_ = belevingsvlucht.plot(ax0)
    belevingsvlucht.plot(
        ax2, color=ret.get_color(), linewidth=2
    )

    ret, *_ = airbus_tree.plot(ax0)
    airbus_tree.plot(
        ax3, color=ret.get_color(), linewidth=2
    )

    # We reduce here the extent of the EuroPP() map
    # between 8°W and 18°E, and 40°N and 60°N
    ax0.set_extent((-8, 18, 40, 60))

    params = dict(fontname="Ubuntu", fontsize=18, pad=12)

    ax0.set_title("EuroPP()", **params)
    ax1.set_title("Lambert93()", **params)
    ax2.set_title("Amersfoort()", **params)
    ax3.set_title("GaussKruger()", **params)

    fig.tight_layout()
    plt.show()
