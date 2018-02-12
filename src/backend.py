import time
#TODO: Enable sense_hat when on production
#from sense_hat import SenseHat
#NB: only use sense_emu for emulation testing
#from sense_emu import SenseHat
import sys
import calendar
import threading

class DataBlock(object):
    __slots__ = ('time','temp_raw', 'temp_cal_h', 'temp_cal_p', 'humidity', 'pressure', 'orientation', 'magneto_raw','magneto', 'gyro', 'accel')

    def __init__(self):
        #TODO: fix calendar formatting for file write
        self.time = calendar.timegm(time.gmtime())
        self.temp_raw = 0
        self.temp_cal_h = 0
        self.temp_cal_p = 0
        self.humidity = 0
        self.pressure = 0
        self.orientation = {}
        self.magneto_raw = {}
        #TODO: Call compass function for below
        self.magneto = 0 
        self.gyro = {}
        self.accel = {}

#Taken from: http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
class RBStatus(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Get status update
            time.sleep(self.interval)
        

class RBCamera(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        from picamera import PiCamera
        i = 0
        with PiCamera() as camera:
            filename = "test1{0}.h264".format(calendar.timegm(time.gmtime()))
            camera.resolution = (1920,1080)
            camera.start_recording(filename)
            camera.wait_recording(5)
            while(True):
                try:
                    filename = "test1{0}.h264".format(calendar.timegm(time.gmtime()))
                    camera.split_recording(filename)
                    camera.wait_recording(5)
                except Exception:
                    #camera.stop_preview()
                    camera.stop_recording()
                    camera.close()
        '''
        #testing
        while true:
            from msvcrt import getch 
            from picamera import PiCamera
            camera = PiCamera(resolution=(1640,922))
            camera.start_recording('test.h264')
            camera.wait_recording(5)
            key = 0
            counter = 1;
            #27 is esc key
            while key != 27:
                key = ord(getch())
                camera.split_recording('test%d.h264' % counter)
                camera.wait_recording(5)
                counter += 1
            camera.stop_recording()
            break
        '''

class FlightComputer():

    session_time = calendar.timegm(time.gmtime())
    raspberry_status = RBStatus(interval=100)
    raspberry_camera = RBCamera(interval=5)
    sense_parent = SenseHat()
    
    def __init__(self):
        self.value = 0
        print("Starting up flight computer...")
        #TODO:REMOVE below
        self.job()

    def print(self, __data__):
        if(type(__data__) == DataBlock):
            try:
                print(__data__.time)
                print("temperature: %s" % __data__.temp_raw)
                print("temperature (computed from humidity): %s" % __data__.temp_cal_h)
                print("temperature (computer from pressure): %s" % __data__.temp_cal_p)
                print("humidity: %s" % __data__.humidity)
                print("pressure: %s" % __data__.pressure)
                print("orientation: %s" % __data__.orientation)
                print("magnetometer: %s" % __data__.magneto)
                print("\n")
                #TODO: Add gyro and accel outputs to writing and output
            except (RuntimeError, NameError, ValueError, KeyboardInterrupt) as e:
                print(e)
        else:
            raise TypeError('__data__ was some type other than backend.FlightComputer. __data__ is currently a {0}'.format(type(__data__)))

    def write(self, file, __data__):        
        if(type(__data__) == DataBlock):
            try:
                #TODO: Convert to JSON format
                self.print(__data__)
                file.write("\"%s\":[\n" % __data__.time)
                file.write("\"temp\": %s,\n" % __data__.temp_raw)
                file.write("\"temp_h\": %s,\n" % __data__.temp_cal_h)
                file.write("\"temp_p\": %s,\n" % __data__.temp_cal_p)
                file.write("\"humidity\": %s,\n" % __data__.humidity)
                file.write("\"pressure\": %s,\n" % __data__.pressure)
                file.write("\"orientation\": %s,\n" % __data__.orientation)
                file.write("\"magneto\": %s,\n" % __data__.magneto)
                file.write("]\n")
                #file.write()
            except Exception as e:
                print("T")
                self.json_setup(file, isEnd = 1)
                print(e)
        else:
            raise TypeError('__data__ was some type other than backend.DataBlock. __data__ is currently a {0}'.format(type(__data__)))
    
    def collect(self, sense):
        _data_ = DataBlock()
        
        try:
            #TODO: Remove pass
            #pass
            _data_.humidity = sense.get_humidity()
            _data_.temp_cal_h = sense.get_temperature_from_humidity()
            _data_.temp_cal_p = sense.get_temperature_from_pressure()
            _data_.temp_raw = (_data_.temp_cal_h + _data_.temp_cal_p)/2
            _data_.pressure = sense.get_pressure()
            #get_orientation is in degrees (calls get_orientation_degrees)
            _data_.orientation = sense.get_orientation()
            _data_.magneto_raw = sense.get_compass_raw()
            _data_.magneto = sense.get_compass()
            _data_.gyro = sense.get_gyroscope()
            _data_.accel = sense.get_accelerometer()
            return _data_
        except Exception as e:
            print(e)
        return _data_

    def job(self):
        
        obj_name = "_session_{0}.txt".format(self.session_time)

        with open(obj_name, 'w+') as file:
            self.json_setup(file)
            while(True):
                self.write(file, self.collect(self.sense_parent))
                #TODO: Temporary statment below
                time.sleep(1)
        return 0
    
    def json_setup(self, file, isEnd = 0):
        if(isEnd == 0):
            try:
                file.write("{\n")
                file.write("\"data\":{")
            except (RuntimeError, NameError, ValueError, KeyboardInterrupt) as e:
                print(e)
        elif(isEnd == 1):
            try:
                file.write("},\n")
                file.write("\"meta\": {\n")
                file.write("}\n")
                file.write("}\n")
            except (RuntimeError, NameError, ValueError, KeyboardInterrupt) as e: 
                print(e)
