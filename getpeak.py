import glob
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import differential_evolution
from numpy import genfromtxt
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
import matplotlib.pyplot as plt
from lmfit.models import *

def get_peak(x,y):
    # bounds on parameters are set in generate_Initial_Parameters() below
    def double_Lorentz(x, a, b, A, w, x_0, A1, w1, x_01):
        return a * x + b + (2 * A / np.pi) * (w / (4 * (x - x_0) ** 2 + w ** 2)) + (2 * A1 / np.pi) * (
                w1 / (4 * (x - x_01) ** 2 + w1 ** 2))

    # function for genetic algorithm to minimize (sum of squared error)
    # bounds on parameters are set in generate_Initial_Parameters() below
    def sumOfSquaredError(parameterTuple):
        warnings.filterwarnings("ignore")  # do not print warnings by genetic algorithm
        return np.sum((yData - double_Lorentz(xData, *parameterTuple)) ** 2)

    def generate_Initial_Parameters():
        # min and max used for bounds
        maxX = max(xData)
        minX = min(xData)
        maxY = max(yData)
        minY = min(yData)

        test = 50
#        if maxY > 33500:
#            test = 40

        parameterBounds = []
        parameterBounds.append([-1.0, 1.0])  # parameter bounds for a
        parameterBounds.append([maxY / -2.0, maxY / 2.0])  # parameter bounds for b
        # change parameter
        parameterBounds.append([0.0, maxY * test])  # parameter bounds for A
        parameterBounds.append([0.0, maxY / 2.0])  # parameter bounds for w
        parameterBounds.append([minX, maxX])  # parameter bounds for x_0
        parameterBounds.append([0.0, maxY * test])  # parameter bounds for A1
        parameterBounds.append([0.0, maxY / 2.0])  # parameter bounds for w1
        parameterBounds.append([minX, maxX])  # parameter bounds for x_01

        # "seed" the numpy random number generator for repeatable results
        result = differential_evolution(sumOfSquaredError, parameterBounds, seed=3)
        return result.x

    width = 180
<<<<<<< HEAD
    index = peakutils.peak.indexes(y, thres=01, min_dist=100)
=======
    index = peakutils.peak.indexes(y, thres=0.5, min_dist=100)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
    index = index[1:]
    print("X index:", x[index], "Y index:", y[index])
    peaks_y = peakutils.interpolate(x, y, ind=index, width=width)
    print("Interpolated:", peaks_y)

    range_left = int(index - width)
    range_right = int(index + width + 1)
    xdata = np.array(x[range_left:range_right])
    ydata = np.array(y[range_left:range_right])

    xData = xdata
    yData = ydata





    # generate initial parameter values
    initialParameters = generate_Initial_Parameters()

    # curve fit the test data
    fittedParameters, pcov = curve_fit(double_Lorentz, xData, yData, initialParameters)

    # create values for display of fitted peak function
    a, b, A, w, x_0, A1, w1, x_01 = fittedParameters
    y_fit = double_Lorentz(xData, a, b, A, w, x_0, A1, w1, x_01)
#    print("Max Y value:", max(yData))
#    print("Max Y value after fitting:", max(y_fit))
<<<<<<< HEAD
    index = peakutils.peak.indexes(y_fit, thres=01, min_dist=400)
=======
    index = peakutils.peak.indexes(y_fit, thres=0.5, min_dist=400)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
#    index = index[1:]

    print("X index:", xData[index], "Y index:", y_fit[index])

#    plt.plot(x, y)  # plot the raw data
#    plt.plot(xData, y_fit)  # plot the equation using the fitted parameters
#    pplot(xData, y_fit, index)
#    pyplot.title('Double Lorentzian Model)')
#    pyplot.ylabel('Amplitude(AUD)')
#    pyplot.xlabel('Wavelength(nm)')
#    plt.show()
    # print(fittedParameters)
    return y_fit[index]

def org_peak(x,y):
<<<<<<< HEAD
    index = peakutils.peak.indexes(y, thres=01, min_dist=100)
=======
    index = peakutils.peak.indexes(y, thres=0.5, min_dist=100)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
    index = index[:1]
    print(y[index])
    return x[index]

def lorentzian_peak(x,y):
    width = 200
<<<<<<< HEAD
    index = peakutils.peak.indexes(y, thres=01, min_dist=100)
=======
    index = peakutils.peak.indexes(y, thres=0.5, min_dist=100)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
    index = index[1:]
    print("X index:", x[index], "Y index:", y[index])
    peaks_y = peakutils.interpolate(x, y, ind=index, width=width)
    print("Interpolated:", peaks_y)

    range_left = int(index - width)
    range_right = int(index + width + 1)
    xdata = np.array(x[range_left:range_right])
    ydata = np.array(y[range_left:range_right])

    gmodel = LorentzianModel()
    params = gmodel.make_params(cen=x[index], amp=y[index], wid=width, sigma=x.std())
    result = gmodel.fit(ydata, params, x=xdata)
#    print(f_result.fit_report())
    print(result.values['height'])
    print(result.values['center'])
#    return f_result.values['height']
    return result.values['center']


def fetch_peak():
    path = r"/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/0_filtered/*.csv"
    wls = genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/wls.csv")
    counter = 0
    df = pd.DataFrame()
    li = np.array([])
    ti = np.array([])
    for fname in sorted(glob.glob(path)):
        specf = genfromtxt(fname)
        print(fname)
        #    print("Interpolated:", peaks_y)
        timestamp = str(fname.split('.')[0].split('_')[4])
        print(timestamp)
        ti = np.append(ti, timestamp)
        li = np.append(li, get_peak(wls, specf))
        #    print(type(timestamp))
        counter = counter + 1
        print((counter/111)*100, '%')

    ti = ti.astype(np.int)

    fi = np.concatenate((ti.reshape(-1, 1), li.reshape(-1, 1)), axis=1)

    df = pd.DataFrame(fi)
    df.to_csv(f"/home/suzon/Work/New_Files/Short_Run/2ndramanamp.csv", header=False, index=False)
    print(df)


fetch_peak()