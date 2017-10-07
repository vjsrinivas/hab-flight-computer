import time
# Enable sense_hat when on production
#from sense_hat import SenseHat
import sys
import calendar

class DataBlock(object):
    __slots__ = ('time','temp_raw', 'temp_cal', 'humidity', 'pressure', 'orientation', 'magneto')

    def __init__(self, x=0, y=0, z=0):
        #TODO: fix calendar formatting for file write
        self.time = calendar.timegm(time.gmtime())
        self.temp_raw = 0
        self.temp_cal = 0
        self.humidity = 0
        self.pressure = 0
        self.orientation = [x,y,z]
        self.magneto = 0
        

class FlightComputer():

    session_time = calendar.timegm(time.gmtime())
    
    def __init__(self):
        self.value = 0
        print("Starting up flight computer...")
        #REMOVE below
        self.job()

    def print(self, __data__):
        if(type(__data__) == DataBlock):
            print(__data__.time)
            print(
                "temperature: {0}\ntemperature (computed): {1}\nhumidity: {2}\npressure: {3}\norientation: {4}\nmagnetometer: {5}"
                .format(__data__.temp_raw, __data__.temp_raw, __data__.humidity, __data__.pressure, __data__.orientation, __data__.magneto)
            )
        else:
            raise TypeError('__data__ was some type other than backend.FlightComputer. __data__ is currently a {0}'.format(type(__data__)))

    def write(self, __data__):
        obj_name = "_session_{0}.txt".format(self.session_time)
        
        if(type(__data__) == DataBlock):
            try:
                file = open(obj_name, 'w+')
                file.write(
                    "temperature: {0}\ntemperature (computed): {1}\nhumidity: {2}\npressure: {3}\norientation: {4}\nmagnetometer: {5}"
                    .format(__data__.temp_raw, __data__.temp_raw, __data__.humidity, __data__.pressure, __data__.orientation, __data__.magneto)
                )
            except:
                pass
        else:
            raise TypeError('__data__ was some type other than backend.FlightComputer. __data__ is currently a {0}'.format(type(__data__)))
    
    def job(self):
        while(True):
            self.write(DataBlock())
        return 0