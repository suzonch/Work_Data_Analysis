import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import differential_evolution
from numpy import genfromtxt
from peakutils.plot import plot as pplot
import peakutils

# Double Lorentzian peak function
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
#    if maxY > 33500:
#        test = 40


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



#yData = genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/0_filtered/filteredSpec_1556200568.csv")
#xData = genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/wls.csv")


y = genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/0_filtered/filteredSpec_1556200954.csv")
x = genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/wls.csv")
width = 200
<<<<<<< HEAD
index= peakutils.peak.indexes(y, thres= 01, min_dist=100)
=======
index= peakutils.peak.indexes(y, thres= 0.5, min_dist=100)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
index = index[1:]
print("X index:",x[index],"Y index:", y[index])
peaks_y = peakutils.interpolate(x, y, ind=index, width= width)
print("Interpolated:", peaks_y)

range_left = int(index - width)
range_right = int(index + width +1)
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
print("Max Y value:",max(yData))
print("Max Y value after fitting:",max(y_fit))
index= peakutils.peak.indexes(y_fit, thres= 0.05, min_dist=100)
#index = index[1:]

print("X index:", xData[index], "Y index:", y_fit[index])

plt.plot(x, y)  # plot the raw data
plt.plot(xData, y_fit)  # plot the equation using the fitted parameters
pplot(xData, y_fit, index )
pyplot.title('Raman Spectroscopy-Double Lorentzian(Filtered)')
pyplot.ylabel('Amplitude(AUD)')
pyplot.xlabel('Wavelength(nm)')
plt.show()

#print(fittedParameters)