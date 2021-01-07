import time
from argparse import ArgumentParser, FileType
from logging import Formatter, StreamHandler, getLogger, DEBUG, ERROR
from sys import modules, stderr
from traceback import format_exc
from pyftdi import FtdiLogger
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController, I2cNackError
from pyftdi.misc import add_custom_devices
from pyftdi.ftdi import Ftdi
import pyftdi.i2c


ftdi = Ftdi.show_devices()

print(ftdi)

#print(ftdi)

i2c = pyftdi.i2c.I2cController()
i2c.configure('ftdi://ftdi:232h/1')

def scan():
    for i in range(255):
        r = i2c.poll(i)
        if r:
            print(i)


dac = i2c.get_port(0xc)
adc = i2c.get_port(0x50)

#print(dac.poll())


#print("DAC:", dac.read(1))


#adc.write(b'')

adc.write(0b0)
#time.sleep(1)
#print("ADC:", adc.read())

 
def read():
    while True:
        time.sleep(.3)
        meas = adc.read(2)
        print(meas)
        m16 = ((meas[0]) << 8) | meas[1]
        val = m16 & 0b0000111111111100
        adc_val = val >> 2
        print(bin(adc_val))
        print(adc_val / pow(2, 10) * 5)

#scan()

read()