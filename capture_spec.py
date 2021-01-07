from avaspec import *
import time
from array import array
#from stepper_control import *
import os.path
import datetime
from threading import Timer
from datetime import datetime, timedelta

AVS_Init(0)
print('Found %d devices' % AVS_GetNrOfDevices())
idtype = AvsIdentityType *1
devs = AVS_GetList(75, 0, idtype)
sn = str(devs[1].SerialNumber.decode('utf-8'))
dev_h = AVS_Activate(devs[1])
dev_cfg_t = DeviceConfigType
dev_cfg = AVS_GetParameter(dev_h, 63484, 0, dev_cfg_t)
pixel_count = dev_cfg[1].m_Detector_m_NrPixels
print('Pixel count: %d' % pixel_count)

def measure(integration_time):
        ret = AVS_UseHighResAdc(dev_h, True)
        measconfig = MeasConfigType
        measconfig.m_StartPixel = 0
        measconfig.m_StopPixel = pixel_count - 1
        measconfig.m_IntegrationTime = integration_time
        measconfig.m_IntegrationDelay = 0
        measconfig.m_NrAverages = int(5)
        measconfig.m_CorDynDark_m_Enable = 0 # nesting of types does NOT work!!
        measconfig.m_CorDynDark_m_ForgetPercentage = 0
        measconfig.m_Smoothing_m_SmoothPix = 0
        measconfig.m_Smoothing_m_SmoothModel = 0
        measconfig.m_SaturationDetection = 0
        measconfig.m_Trigger_m_Mode = 0
        measconfig.m_Trigger_m_Source = 0
        measconfig.m_Trigger_m_SourceType = 0
        measconfig.m_Control_m_StrobeControl = 0
        measconfig.m_Control_m_LaserDelay = 0
        measconfig.m_Control_m_LaserWidth = 0
        measconfig.m_Control_m_LaserWaveLength = 0.0
        measconfig.m_Control_m_StoreToRam = 0
        ret = AVS_PrepareMeasure(dev_h, measconfig)
        nummeas = int(1)
        # ret = AVS_MeasureCallback(globals.dev_handle, ctypes.addressof(callbackclass.callback(self, 0, 0)),
        # nummeas)
        scans = 0
        while (scans < nummeas):
            ret = AVS_Measure(dev_h, 0, 1)
            dataready = False
            while (dataready == False):
                dataready = (AVS_PollScan(dev_h) == True)
                time.sleep(0.001)
            if (dataready == True):
                scans = scans + 1
                ts = 0
                specData = []
                resp = AVS_GetScopeData(dev_h, ts, specData)
                ts = resp[0]
                for idx in range(pixel_count):
                     #specData[idx] = resp[1][idx]
                     specData.append(resp[1][idx])
                return specData
            scans = scans + 1

#Integation time
tt= 100

#print(spec)
#AVS_Done(0)
#def save_spec(data):
#    ts = time.time()
#    with open(os.path.join('output/LED1','spec_%d.csv' %ts), 'w') as f:
#        for i in measure(tt):
#            f.write('%d\n' %i)

"""
def capture():
    time.sleep(.6)
    count = int(0)
    for _ in range(9):

        count = count +1

        if count == 1:
            ts = time.time()
            with open(os.path.join('output/Dark', 'dark_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 2:
            ts = time.time()
            with open(os.path.join('output/LED1', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 3:
            ts = time.time()
            with open(os.path.join('output/LED2', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 4:
            ts = time.time()
            with open(os.path.join('output/LED3', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 5:
            ts = time.time()
            with open(os.path.join('output/LED4', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 6:
            ts = time.time()
            with open(os.path.join('output/LED5', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 7:
            ts = time.time()
            with open(os.path.join('output/LED6', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 8:
            ts = time.time()
            with open(os.path.join('output/LED7', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)


        if count == 9:
            ts = time.time()
            with open(os.path.join('output/LED8', 'spec_%d.csv' % ts), 'w') as f:
                for i in measure(tt):
                    f.write('%d\n' % i)

        time.sleep(1.5)

        print("Capture", count)
    time.sleep(3.8)

def repeat_capture():
    for _ in range(1):
        capture()


def timerc():
    x = datetime.today()
    y = x.replace(day=x.day, hour=10, minute=11, second=0, microsecond=0) + timedelta(days=0)
    delta_t = y - x

    secs = delta_t.total_seconds()

    t = Timer(secs, repeat_capture)
    t.start()


#timerc()
#repeat_capture()

"""
