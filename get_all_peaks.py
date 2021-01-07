import glob
import pandas as pd
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import differential_evolution
from numpy import genfromtxt
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
import matplotlib.pyplot as plt
from lmfit.models import *

def get_raman_peak(x,y):
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

        test = 20
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

    width = 200
    index = peakutils.peak.indexes(y, thres=01, min_dist=100)
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
    index = peakutils.peak.indexes(y_fit, thres=01, min_dist=400)
#    index = index[1:]

    print("X index:", xData[index], "Y index:", y_fit[index])

    plt.plot(x, y)  # plot the raw data
    plt.plot(xData, y_fit)  # plot the equation using the fitted parameters
    pplot(xData, y_fit, index)
    pyplot.title('Double Lorentzian Model)')
    pyplot.ylabel('Amplitude(AUD)')
    pyplot.xlabel('Wavelength(nm)')
#    plt.show()
    # print(fittedParameters)
    return xData[index]



def lorentzian_peak(x,y):

    def lorentzian_model(x, y):
        width = 200
        index = peakutils.peak.indexes(y, thres=01, min_dist=100)
#        index = index[1:]
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
#        print(result.fit_report())
        print(result.values['height'])
        print(result.values['center'])

#        result.plot_fit()
        # plt.plot(xdata, f_result.best_fit, 'r-', label='best fit')
#        pplot(x, y, index, )
#        pyplot.title('Lorentzian Model')
#        pyplot.ylabel('Amplitude(AUD)')
#        pyplot.xlabel('Wavelength(nm)')
#        plt.legend(loc='best')
#        pyplot.show()

        return np.array([result.values['height'], result.values['center']])

    def lorentzian_window(x,y):

        interpolation_window = 150  # recommanded to keep same as second_window

        index = peakutils.peak.indexes(y, thres=01, min_dist=100)
        print("X index:", x[index], "Y index:", y[index])
        peaks_y = peakutils.interpolate(x, y, ind=index, width=interpolation_window)
        print("Interpolated:", peaks_y)

        first_window = 40
        second_window = 100

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
        #    print(f_result.fit_report())
        print(f_result.values['height'])
        print(f_result.values['center'])

        s_gmodel = LorentzianModel()
        s_params = s_gmodel.make_params(cen=x[index[1:]], amp=y[index[1:]],
                                        wid=second_window, sigma=5)
        s_result = s_gmodel.fit(s_ydata, s_params, x=s_xdata)
        #    print(s_result.fit_report())
        print(s_result.values['height'])
        print(s_result.values['center'])

        f_result.plot_fit()
        s_result.plot_fit()
        pplot(x, y, index)
        pyplot.title('Lorentzian Model')
        pyplot.ylabel('Amplitude(AUD)')
        pyplot.xlabel('Wavelength(nm)')
        plt.legend(loc='best')
        pyplot.show()

        return np.array([f_result.values['height'], f_result.values['center'],
                         s_result.values['height'], s_result.values['center']])


    return lorentzian_model(x,y)



def org_peak(x,y):
    index = peakutils.peak.indexes(y, thres=01, min_dist=100)
    print(y[index])
    return np.array([y[index[:1]], x[index[:1]], y[index[1:]], x[index[1:]]])

def fetch_peak():
    path = r"/home/suzon/Work/LED_tests/short_run/MTE9440N/led1/0_filtered/*.csv"
    wls = genfromtxt("/home/suzon/Work/LED_tests/short_run/MTE9440N/led1/wls.csv")
    counter = 0
    fstpeak = np.array([])
    fstwave = np.array([])
#    sndpeak = np.array([])
#    sndwave = np.array([])
    ti = np.array([])
    for fname in sorted(glob.glob(path)):
        specf = genfromtxt(fname)
        print(fname)
        #    print("Interpolated:", peaks_y)
        timestamp = str(fname.split('.')[0].split('_')[4])
#        print(timestamp)
        ti = np.append(ti, timestamp)
        fstpeak = np.append(fstpeak, lorentzian_peak(wls, specf)[0])
        fstwave = np.append(fstwave, lorentzian_peak(wls, specf)[1])
#        sndpeak = np.append(sndpeak, lorentzian_peak(wls, specf)[2])
#        sndwave = np.append(sndwave, lorentzian_peak(wls, specf)[3])
        #    print(type(timestamp))
        counter = counter + 1
        print((counter/110)*100, '%')

    ti = ti.astype(np.int)

    fi = np.concatenate((ti.reshape(-1, 1), fstpeak.reshape(-1, 1),fstwave.reshape(-1, 1)), axis=1)

#    fi = np.concatenate((ti.reshape(-1, 1), fstpeak.reshape(-1, 1),fstwave.reshape(-1, 1),
#                         sndpeak.reshape(-1, 1), sndwave.reshape(-1, 1)), axis=1)

    df = pd.DataFrame(fi)
    df.to_csv(f"/home/suzon/Work/New_Files/Short_Run/loren_mte9440n_led1_0.csv", header=False, index=False)
    print(df)


fetch_peak()