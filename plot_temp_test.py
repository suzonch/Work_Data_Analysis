from numpy import genfromtxt
import numpy as np
import numpy
import matplotlib.pyplot as plt
from scipy import signal


s = genfromtxt("/home/suzon/Work/Temp_test/Temp_Chart.csv", delimiter=',')


set_point = s[:,0]
resistance = s[:,1]
temp = s[:,2]
therm_volt = s[:,3]



def plot4(set_point, resistance,temp,therm_volt):
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    fig, host = plt.subplots()
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    par2.spines["right"].set_position(("axes", 1.1))
    par3.spines["right"].set_position(("axes", 1.3))

    make_patch_spines_invisible(par2)
    make_patch_spines_invisible(par3)

    par2.spines["right"].set_visible(True)
    par3.spines["right"].set_visible(True)

    p1, = host.plot(set_point, resistance, "b-", label="External NTC Resistance")
    p2, = par1.plot(set_point, temp, "r-", label="Temperature in C")
    p3, = par2.plot(set_point, therm_volt, "g-", label="Thermistor Voltage (mV)")


    host.set_xlabel("Set Point (mV)")
    host.set_ylabel("External NTC Resistance")
    par1.set_ylabel("Temperature in C")
    par2.set_ylabel("Thermistor Voltage (mV)")


    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=11)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p2, p3]

    host.legend(lines, [l.get_label() for l in lines])
    plt.show()



plot4(set_point, resistance, temp, therm_volt)