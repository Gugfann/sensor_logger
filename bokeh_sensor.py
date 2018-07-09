# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
from bokeh.layouts import column
import wiringpi as w
import time
import struct
from collections import deque
from sensor import Sensor

p1 = figure(plot_width=1000, plot_height=400, y_range=(0,100))
p2 = figure(plot_width=1000, plot_height=400)#, y_range=(0,100))

x1 = deque([0]*200,200)
x2 = deque([0]*200,200)
y1 = deque([0]*200,200)
y2 = deque([0]*200,200)

y12 = deque([0]*200,200)
y22 = deque([0]*200,200)

r1 = p1.line(x1, y1, color="firebrick", line_width=2)
r2 = p1.line(x2, y2, color="navy", line_width=2)
ds1 = r1.data_source
ds2 = r2.data_source

r12 = p2.line(x1, y12, color="firebrick", line_width=2)
r22 = p2.line(x2, y22, color="navy", line_width=2)
ds12 = r12.data_source
ds22 = r22.data_source

channel = 0
speed = 500000 
dt = 0.001

w.wiringPiSPISetup(channel, speed)
# only the first 5 bits are relevant the rest we don't care about 
# Channel 0 01101XXX XXXXXXXX
# Channel 1 01111XXX XXXXXXXX
channel0_select = 'hE'
channel1_select = 'xE'

sensor1 = Sensor(channel0_select,'Sensor 1')
sensor2 = Sensor(channel1_select,'Sensor 2')

t0 = time.time()

@linear()
def update(step):
    global x1,x2,y1,y2
    global t0
    
    s1 = sensor1.read()
    s2 = sensor2.read()

    x1.append(step)
    x2.append(step)
    y1.append(s1)
    y2.append(s2)

    ds1.data['x'] = x1
    ds1.data['y'] = y1
    ds2.data['x'] = x2
    ds2.data['y'] = y2
    ds1.trigger('data', ds1.data, ds1.data)
    ds2.trigger('data', ds2.data, ds2.data)

    dydt1 = (s1 - y1[-2])/dt
    dydt2 = (s2 - y2[-2])/dt

    y12.append(dydt1)
    y22.append(dydt2)

    ds12.data['x'] = x1
    ds12.data['y'] = y12
    ds22.data['x'] = x2
    ds22.data['y'] = y22
    ds12.trigger('data', ds12.data, ds12.data)
    ds22.trigger('data', ds22.data, ds22.data)


curdoc().add_root(column(p1,p2))

# Add a periodic callback to be run every 70 milliseconds
curdoc().add_periodic_callback(update, dt*1000)