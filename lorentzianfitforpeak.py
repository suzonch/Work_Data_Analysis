from lmfit.models import *
import peakutils
import numpy as np
import matplotlib.pyplot as plt
from peakutils.plot import plot as pplot
from matplotlib import pyplot
from numpy import genfromtxt

def lorentzian_model(x,y):
    width = 200
<<<<<<< HEAD
    index = peakutils.peak.indexes(y, thres=01, min_dist=100)
=======
    index = peakutils.peak.indexes(y, thres=0.5, min_dist=100)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
    print("X index:", x[index], "Y index:", y[index])
    peaks_y = peakutils.interpolate(x, y, ind=index, width=width)
    print("Interpolated:", peaks_y)

    range_left = int(index - width)
    range_right = int(index + width + 1)
    xdata = np.array(x[range_left:range_right])
    ydata = np.array(y[range_left:range_right])

    gmodel = LorentzianModel()
    params = gmodel.make_params(cen=x[index], amp=y[index], wid=width, sigma=5)
    result = gmodel.fit(ydata, params, x=xdata)
    print(result.fit_report())
    print(result.values['height'])
    print(result.values['center'])

    result.plot_fit()
    # plt.plot(xdata, f_result.best_fit, 'r-', label='best fit')
    pplot(x, y, index, )
    pyplot.title('Lorentzian Model')
    pyplot.ylabel('Amplitude(AUD)')
    pyplot.xlabel('Wavelength(nm)')
    plt.legend(loc='best')
    pyplot.show()

def lorentzian_window(x,y):

    interpolation_window = 150  # recommanded to keep same as second_window

<<<<<<< HEAD
    index = peakutils.peak.indexes(y, thres=01, min_dist=100)
=======
    index = peakutils.peak.indexes(y, thres=0.5, min_dist=100)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
    print("X index:", x[index], "Y index:", y[index])
    peaks_y = peakutils.interpolate(x, y, ind=index, width=interpolation_window)
    print("Interpolated:", peaks_y)

    first_window = 20
    second_window = 150

    f_range_left = int(index[:1] - first_window)
    f_range_right = int(index[:1] + first_window + 1)
    f_xdata = np.array(x[f_range_left:f_range_right])
    f_ydata = np.array(y[f_range_left:f_range_right])

    s_range_left = int(index[1:] - second_window)
    s_range_right = int(index[1:] + second_window + 1)
    s_xdata = np.array(x[s_range_left:s_range_right])
    s_ydata = np.array(y[s_range_left:s_range_right])

    f_gmodel = LorentzianModel()
    f_params = f_gmodel.make_params(cen=x[index[:1]], amp=y[index[:1]],
                                    wid=first_window, sigma=5)
    f_result = f_gmodel.fit(f_ydata, f_params, x=f_xdata)
    print(f_result.fit_report())
    print(f_result.values['height'])
    print(f_result.values['center'])

    s_gmodel = LorentzianModel()
    s_params = s_gmodel.make_params(cen=x[index[1:]], amp=y[index[1:]],
                                    wid=second_window, sigma=s_xdata.std())
    s_result = s_gmodel.fit(s_ydata, s_params, x=s_xdata)
    print(s_result.fit_report())
    print(s_result.values['height'])
    print(s_result.values['center'])


    f_result.plot_fit()
    s_result.plot_fit()
    pplot(x, y, index, )
    pyplot.title('Lorentzian Model')
    pyplot.ylabel('Amplitude(AUD)')
    pyplot.xlabel('Wavelength(nm)')
    plt.legend(loc='best')
    pyplot.show()


y = genfromtxt("/home/suzon/Work/LED_tests/short_run/MTE9440N/led1/0_filtered/filteredSpec_1556778007.csv")
x = genfromtxt("/home/suzon/Work/LED_tests/short_run/MTE9440N/led1/wls.csv")


lorentzian_model(x,y)