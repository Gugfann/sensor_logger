import wiringpi as w
import time
import struct
from math import log
from datetime import datetime

from fsm import FSM
from sensor import Sensor

channel = 0
speed = 500000 

w.wiringPiSPISetup(channel, speed)
# only the first 5 bits are relevant the rest we don't care about 
# Channel 0 01101XXX XXXXXXXX
# Channel 1 01111XXX XXXXXXXX
channel0_select = 'hE'
channel1_select = 'xE'

sensor1 = Sensor(channel0_select,'Sensor 1')
sensor2 = Sensor(channel1_select,'Sensor 2')

fsm = FSM(20,30)

while True:
    s1 = sensor1.read()
    s2 = sensor2.read()

    object_found = fsm.update(s1,s2)

    if object_found:
        print('... and another one!')

        now = datetime.now()

        print(str(now) + "\n")
        with open("log.txt","a") as file:
            file.write(str(now) + "\n")


   # print("Sensor 1: {}\nSensor 2: {}".format(s1, s2)) 
    time.sleep(0.05)
