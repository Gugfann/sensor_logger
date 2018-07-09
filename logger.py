import wiringpi as w
import time
import struct
from math import log
from datetime import datetime
from collections import deque
import numpy as np

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

# sensor0 = Sensor(channel0_select, 'Sensor 0', calibrate=False)
sensor = Sensor(channel1_select, 'Sensor 1', calibrate=True)

N = 60

history = deque([0]*N,N)

high = 75
low = 70

state_hi = False
no_of_objects = 0

t0 = time.time()

f = open("data.txt","w")

f.close()

counter = 0

while True:
    value = sensor.read(boost=True)
    # uncalibrated = sensor0.read(boost=True)
    # background = sensor0.read(boost=True)

    history.append(value)
    filtered = np.mean(history)

    # with open("data.txt","a") as f:
    #     f.write("{}\n".format(filtered))

    # time.sleep(0.1)

    object_found = False

    if filtered > high and not state_hi:
        state_hi = True

    if filtered > high:
        counter += 1

    if filtered < low and state_hi:
        state_hi = False

        if counter > 200:
            object_found = True

        print("Sample count: {}".format(counter))
        counter = 0

    if object_found:
        no_of_objects += 1
        print('Object count: {}'.format(no_of_objects))

        now = datetime.now()

        out = "{}, {}, {}, {}, {}, {}, {} \n".format(
                now.year,
                now.month,
                now.day,
                now.hour,
                now.minute,
                now.second,
                now.microsecond)

        print(out)
        with open("log.txt","a") as file:
            file.write(out)

    # t1 = time.time()

    # print("Cycle time: {}".format(t1-t0))
    # t0 = t1
    # print("Sensor 1: {}\nSensor 2: {}".format(s1, s2)) 
    #time.sleep(0.05)
