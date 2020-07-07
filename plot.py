from numpy import genfromtxt
import numpy as np
import numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

x = genfromtxt("/home/suzon/Work/LED_tests/long_run/long_LTW/45_LTW2/iv.csv", delimiter=' ')
t = genfromtxt("/home/suzon/Work/LED_tests/long_run/long_LTW/temp_env.csv", delimiter=' ')


temptemp = (t[0:,1])
temptemp = np.around([temptemp], decimals=2) -23
temptemp = temptemp*100
#print(temptemp)
temp = temptemp.astype(numpy.int64)
temp = temp.reshape(6201)


voltemp = (x[0:,1])-3
voltemp = np.around([voltemp], decimals=3)
voltemp = voltemp*1000
voltage = voltemp.astype(numpy.int64)
voltage = voltage.reshape(6201)

tempcurrent =(x[0:,2])
tempcurrent = (tempcurrent *1000)-30
tempcurrent = np.around([tempcurrent],decimals=2)
tempcurrent = tempcurrent *100
current = tempcurrent.astype((numpy.int64))
current = current.reshape(6201)


