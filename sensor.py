import wiringpi as w
from time import time
import struct
from math import log

class Sensor(object):

    def __init__(self, channel_select, sensor_name, calibrate=True):
        self.channel_select = channel_select
        self.__name__ = sensor_name
        self.offset = 0

        if calibrate:
            self.calibrate()

    def calibrate(self):
        # find the offset for the current light level
        t0 = time()
        t1 = time()

        data = []

        print("Starting calibration for {}".format(self.__name__))

        # find average light level over 2 seconds
        while t1 - t0 < 4:
            data.append(self.get_spi_data())
            t1 = time()
        
        # use the mean light level as the offset
        mean = int(sum(data) / len(data))
        self.offset = mean

        print("Ending calibration for {}".format(self.__name__))

    def get_spi_data(self):
        buf = bytes(self.channel_select.encode('UTF-8'))
        _, data = w.wiringPiSPIDataRW(0, buf)
        byteArr = bytearray(data)
    
        # we only want the lowest 10 bits of the msg si the 6 MSB are masked out
        mask = int('00000011', 2)
        byteArr[0] = mask & byteArr[0]
        a = struct.unpack('>H',byteArr)

        # invert range so close objects have high values and vice versa
        return 1024 - a[0]

    def boost_low_range(self,data):
        # boost the sensor reading so objects far away give a greater response
        value = data - self.offset if (data - self.offset) > 1 else 1
        gamma = 10*log(value)

        # normalize so range goes from 0 to 100 %
        norm_factor = 10*log(1024 - self.offset)
        return int(gamma*100 / norm_factor)

    def read(self,boost=True):
        data = self.get_spi_data()

        if boost == True:
            data = self.boost_low_range(data)

        return data