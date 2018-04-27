from time import time

class FSM(object):

    def __init__(self, t_low, t_high):
        self.state = 'IDLE'
        self.low_thresh = t_low
        self.high_thresh = t_high

        self.states = { 'IDLE': self.idle,
                        'S1HI': self.s1hi,
                        'S2HI': self.s2hi,
                        'HIGH': self.high}

    def idle(self, sensor1, sensor2):
        if sensor1 > self.high_thresh:
            #print('Sensor 1 saw something!')
            self.state = 'S1HI'
        elif sensor2 > self.high_thresh:
            #print('Sensor 2 saw something!')
            self.state = 'S2HI'

    def s1hi(self, sensor1, sensor2):
        if sensor1 < self.low_thresh:
            #print("It's nothing..")
            self.state = 'IDLE'
        elif sensor2 > self.high_thresh:
            #print('Yeah, me too!')
            self.state = 'HIGH'

    def s2hi(self, sensor1, sensor2):
        if sensor2 < self.low_thresh:
            #print("It's nothing..")
            self.state = 'IDLE'
        elif sensor1 > self.high_thresh:
            #print('Yeah, me too!')
            self.state = 'HIGH'

    def high(self, sensor1, sensor2):
        if sensor1 < self.low_thresh and sensor2 < self.low_thresh:
            #print("It's gone now..")
            self.state = 'IDLE'

    def update(self, sensor1, sensor2):
        state = self.state
        self.states[state](sensor1,sensor2)
        
        # if we just changed to the HIGH state, then both sensors have found a new object
        if self.state == 'HIGH' and state != 'HIGH':
            return True

        return False



