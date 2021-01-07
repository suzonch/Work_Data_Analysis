import matplotlib.pyplot as plt
import pandas as pd
from lmfit.models import GaussianModel
from lmfit.models import LorentzianModel
import peakutils
import numpy as np
import pylab as plb
from lmfit import Model
from lmfit.models import VoigtModel
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import csv
from numpy import exp, loadtxt, pi, sqrt
from peakutils.plot import plot as pplot
from matplotlib import pyplot
import numpy
from numpy import genfromtxt

y = genfromtxt("/home/suzon/Work/LED_tests/long_run/long_LTW/45_LTW2_Filtered/spec_filtered_1559809409.csv")
x = genfromtxt("/home/suzon/Work/LED_tests/long_run/long_LTW/wls.csv")
width = 100
index= peakutils.peak.indexes(y, thres= 01, min_dist=400)
print("X index:",x[index],"Y index:", y[index])
peaks_y = peakutils.interpolate(x, y, ind=index, width= width)
print("Interpolated:", peaks_y)


range_left = int(index - width)
range_right = int(index + width +1)
xdata = np.array(x[range_left:range_right])
ydata = np.array(y[range_left:range_right])



gmodel = GaussianModel()
params = gmodel.make_params(cen=x[index], amp=y[index], wid=width, sigma = x.std())
result = gmodel.fit(ydata, params, x=xdata)
print(result.fit_report())
print(xdata.std())
print(x.std())
#print(f_result.best_fit)


pplot(x,y, index,)
pyplot.title('Gaussian Model')
pyplot.ylabel('Amplitude(AUD)')
pyplot.xlabel('Wavelength(nm)')
plt.plot(xdata, result.best_fit, 'r-', label='best fit')
plt.legend(loc='best')
pyplot.show()