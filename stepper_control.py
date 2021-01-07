import serial
import time
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

ser.write(b'?R\r\n')
#time.sleep(.15)
read = ser.readline()
print(read.decode('utf-8'))

#ser.write(b'X-4000\r\n')

def move():
    time.sleep(2)
    for i in range(8):

        ser.write(b'X+4000\r\n')
        time.sleep(2)

        read = ser.readline()
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