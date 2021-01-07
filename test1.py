import serial
from avaspec import *
from capture_spec import *
import time
import os.path
import datetime
from threading import Timer
from datetime import datetime, timedelta

ser = serial.Serial(
                    port = '/dev/ttyUSB0',
                    baudrate = 9600,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    bytesize = serial.EIGHTBITS,
                    xonxoff = False,
                    rtscts = False,
                    dsrdtr = False
)

def adjust():
    ser.isOpen()
    ser.write(b'?R\r\n')
    read = ser.readline()
    print(read.decode('utf-8'))
    time.sleep(1)
    ser.write(b'X-10000\r\n')
    time.sleep(.15)
    read = ser.readline()
    print(read.decode('utf-8'))


#ser.write(b'X-12000\r\n')

#ser.write(b'?R\r\n')
#time.sleep(.15)
#read = ser.readline()
#print(read.decode('utf-8'))



def move():
    time.sleep(4)

    ts = time.time()
    with open(os.path.join('output/Dark', 'dark_%d.csv' % ts), 'w') as f:
        for i in measure(tt):
            f.write('%d\n' % i)



    for i in range(8):

        ser.write(b'X+4000\r\n')
        time.sleep(.20)

        read = ser.readline()

        if read.decode('utf-8') == "OK":
            ts = time.time()
            with open(os.path.join('output/Dark', 'dark_%d.csv' % ts), 'w') as f:
                for i in measure(100):
                    f.write('%d\n' % i)



        time.sleep(2)


        print(read.decode('utf-8'))


    for j in range(1):

        ser.write(b'X-32000\r\n')
        time.sleep(2)

        read = ser.readline()

        print(read.decode('utf-8'))


def start():
    for _ in range(1):
        move()


def timer():
    x = datetime.today()
    y = x.replace(day=x.day, hour=10, minute=11, second=0, microsecond=0) + timedelta(days=0)
    delta_t = y - x

    secs = delta_t.total_seconds()

    t = Timer(secs, start)
    t.start()


#timer()

start()

#adjust()