from lmfit.models import *
import peakutils
import numpy as np
import matplotlib.pyplot as plt
from peakutils.plot import plot as pplot
from matplotlib import pyplot
from numpy import genfromtxt
from scipy import signal

y = genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/0_filtered/filteredSpec_1556200557.csv")
x = genfromtxt("/home/suzon/Work/LED_tests/short_run/FYL-5014UWC1C-15/led1/wls.csv")

width = 50

<<<<<<< HEAD
indexorg= peakutils.peak.indexes(y, thres= 01, min_dist=400)
=======
indexorg= peakutils.peak.indexes(y, thres= 0.5, min_dist=400)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
#print(indexorg)
#indexorg = indexorg[:]
print("Original X index:", x[indexorg], "Original Y index:", y[indexorg])
peaks_y = peakutils.interpolate(x, y, ind=indexorg, width= width)
print("Interpolated Original:", peaks_y)
range_left = int(indexorg - width)
range_right = int(indexorg + width + 1)
xdata = np.array(x[range_left:range_right])
ydata = np.array(y[range_left:range_right])


#b,a = signal.butter(1, 0.095)
#zi = signal.lfilter_zi(b,a)
#ydata, _ = signal.lfilter(b,a, ydata, zi = zi*ydata[0])
#print("Max Y value after filtering:",max(ydata))


<<<<<<< HEAD
#filtered_index = peakutils.peak.indexes(ydata, thres= 01, min_dist=20)
=======
#filtered_index = peakutils.peak.indexes(ydata, thres= 0.5, min_dist=20)
>>>>>>> 675ec615410e69062b0ba2be16b2ca10d58ac332
#print('Filtered x index:', xdata[filtered_index], 'Filtered Y index:', ydata[filtered_index])
#filtered_peaks_y = peakutils.interpolate(xdata, ydata, ind=filtered_index, width= width)
#print("Interpolated Filtered:", filtered_peaks_y)

#width2 = width

#range_left2 = int(filtered_index - width2)
#range_right2 = int(filtered_index + width2 )
#xdatafi = np.array(xdata[range_left2:range_right2])
#ydatafi = np.array(ydata[range_left2:range_right2])


gmodel = LorentzianModel()
params = gmodel.make_params(amplitude =ydata[indexorg] ,center = xdata[indexorg],height = ydata[indexorg], sigma =xdata.std())
print(gmodel.param_names)
result = gmodel.fit(ydata, params, x=xdata)
print(result.fit_report)


#plt.plot(x,y,'o', color = 'green', label = 'Original')
result.plot_fit()
pplot(x, y, indexorg )
pplot(xdata,ydata, filtered_index)
pyplot.title('Lorentzian Model (Filtered)')
pyplot.ylabel('Amplitude(AUD)')
pyplot.xlabel('Wavelength(nm)')
plt.legend(loc='best')
pyplot.show()
