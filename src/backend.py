import time
from sense_hat import SenseHat
import sys

class DataBlock(object):
    __slots__ = ('temp_raw', 'temp_cal', 'humidity', 'pressure', 'orientation', 'magneto')

    def __init__():
        self.temp_raw = 0
        self.temp_cal = 0
        self.humidity = 0
        self.pressure = 0
        self.orientation = [x,y,z]
        self.magneto = 0
        

class FlightComputer():

    def __init__():
        print("Starting up flight computer...")

    def write():
        import calendar
        obj_name = "_session_{0}.txt".format(calendar.timegm(time.gmtime()))
        file = open(obj_name, 'w+')