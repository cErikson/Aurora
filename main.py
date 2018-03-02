# -*- coding: utf-8 -*-
#!/bin/python
"""
Project: Aurora
@author: Christian Erikson

TODO: THE_MOON_IS_BEHIND_SCHEDULE GODS_HELP_US_ALL
TODO: Add fades for sunrise and sunset
TODO: Add ripples
TODO: Add moon phase and weather 
TODO: Hue fader :upsparkels:
TODO: unmagic the moon and sun
TODO: De-miniY2K-ify time_progress
TODO: Demagic dimmer: y=ax+b
TODO: GREEN FLASH!!
"""
##### Debug #####
testing=True

###### Imports #####
import argparse as arg
import pdb
import sys
import time, datetime
import signal
import math
from neopixel import *


##### Args #####
if __name__ == "__main__" and testing != True:
    parser = arg.ArgumentParser()
    # Positional mandatory arguments
    parser.add_argument("srh", help="Sun Rise Hour", type=int)
    parser.add_argument("srm", help="Sun Rise Min", type=int)
    parser.add_argument("ssh", help="Sun Set Hour", type=int)
    parser.add_argument("ssm", help="Sun Set Min", type=int)
    parser.add_argument("preshow", help="Dusk/Dawn Mins Time", type=int)
    parser.add_argument("show", help="Sunset/Sunrise Mins Time", type=int)
    # Optional arguments
    #parser.add_argument("-d", "--indel", help="Gap Penalty", type=int, default=None)
    #parser.add_argument("-a", "--alignment", help="Output Alignment", action='store_true')
    # Parse arguments
    ARGS = parser.parse_args()
    
##### Testing #####
else:   # Else test
    sys.stderr.writelines("!!!!!___RUNNING_IN_TESTING_MODE_WITH_TEST_ARGS___!!!!!\n")
    class test_args(object):
        srh=6
        srm=00
        ssh=21
        ssm=0
        preshow=60
        show=120      
    ARGS = test_args()

# LED strip configuration:
LED_COUNT      = 78      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_BRG   # Strip type and colour ordering

###### Global Const #####
sun_rise=(ARGS.srh,ARGS.srm)
sun_set=(ARGS.ssh,ARGS.ssm)
preshow=ARGS.preshow*60
show=ARGS.show*60
strip_len=LED_COUNT/2
loop=True

##### Colors #####
daysky=(0,100,128)
nightsky=(36,0,108)
dawnsky=(255,195,0)
risesky=(255,200,0)
setsky=(255,75,0)
dusksky=(30,20,35)
sun=(255,245,0)
moon=(255,255,255)
##### Class #####

##### Defs #####

def normpdf(x, mean, sd):
    """Normal Distrubution Probablity Density Function"""
    var = float(sd)**2
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    denom = (2*math.pi*var)**.5
    return num/denom

def time_progress(start, end, now, rev=False):
    """Return the proportion of the current time delta"""
    delta_time=float(end-start)
    time_since_start=now-start
    # pdb.set_trace() # Transposon Z
    return time_since_start/delta_time if rev is False else 1-(time_since_start/delta_time)

def signal_handler(signal, frame):
        global loop, strip
        print('You pressed Ctrl+C!')
        strip._cleanup()
        loop=False
        
# Define functions which animate LEDs in various ways.
        
def set_all(strip, color, strip_len, mult=1):
    """Make the strip a uniform of color"""
    for i in range(strip_len):       
        strip.setPixelColor(i, Color(int(round(color[0]*mult)), int(round(color[1]*mult)), int(round(color[2]*mult))))

def mover(strip, pos, wid, cut, col):
    """ Move a nomal distubution across the strip"""
    scaler=1/normpdf(pos, pos, wid)
    for x in range(strip_len):
        mult=normpdf(x, pos, wid)*scaler
        if mult > cut:
                strip.setPixelColor(x,Color(*[int(round(y*mult)) for y in col]))
    
def sky(strip, set_time, rise_time, strip_len, preshow_time, show_time):
    ''' preshow and show times in mins'''
    sys.stderr.writelines('               Now:{} Dawn{} Rise:{} Morning:{} Sunset:{} Set:{} Dusk:{}\r'.format(secs,rise_time-preshow_time,rise_time,rise_time+show_time,set_time-preshow_time,set_time,set_time+show_time))
    if secs > (rise_time-preshow_time) and secs < rise_time: # is dawn
        #pos=(preshow_time-(rise_time-secs))/float(preshow_time)
        set_all(strip, dawnsky, strip_len)#, pos)
    
    elif secs > rise_time and secs < (rise_time+show_time): # is morning
        #pos=(show_time+(secs-rise_time))/float(show_time)
        set_all(strip, risesky, strip_len)#, pos)
        
    elif secs > (rise_time+show_time) and secs < (set_time-show_time): # is daytime
        set_all(strip, daysky, strip_len)

    elif secs > (set_time-show_time) and secs < set_time: # is sunset
        #pos=time_progress(set_time-show_time, set_time, secs)
        set_all(strip, setsky, strip_len) #, pos)
    elif secs > set_time and secs < (set_time+preshow_time): #is dusk
        #pos=(preshow_time-(set_time-secs))/float(preshow_time)
        set_all(strip, dusksky, strip_len)#, pos)
    
    elif secs > (set_time+preshow_time) or secs < (rise_time-preshow_time): # is night
        set_all(strip, nightsky, strip_len)
    
    else:
        print('oh shit')


def sun_and_moon(strip, set_time, rise_time, strip_len, size=1):
    """
    sunrise and sunset take (24hour, min)
    """
    if secs > rise_time and secs < set_time: # is daytime
        pos=time_progress(rise_time, set_time, secs)*strip_len
        mover(strip, pos, 1.5, 0.2, sun)
    elif secs > set_time: # is night
        pos=time_progress(set_time, 84600, secs)*strip_len
        mover(strip, pos, 1, 0.1, moon)
    elif secs < rise_time: # is morning 
        pos=time_progress(0, rise_time, secs)*strip_len
        mover(strip, pos, 1, 0.1, moon)

def dimmer(strip, set_time, rise_time, preshow_time, show_time):
    if secs > (rise_time-preshow_time) and secs < (rise_time+show_time): # is dawn/moarning
        pos=time_progress(rise_time-preshow_time, rise_time+show_time, secs)
        strip.setBrightness(int((0.87452*255*pos)+32))
        
    elif secs > (rise_time+show_time) and secs < (set_time-show_time): # is daytime
        strip.setBrightness(255)

    elif secs > (set_time-show_time) and secs < (set_time+preshow_time): # is sunset/dusk
        pos=time_progress(set_time-show_time, set_time+preshow_time, secs, rev=True)
        strip.setBrightness(int((0.87452*255*pos)+32))
        
    elif secs > (set_time+preshow_time) or secs < (rise_time-preshow_time): # is night
        strip.setBrightness(32)
    else:
        print('Arse_1')
        
def strip_show(strip, double=True, reverse=False):
    leds=strip.getPixels()
    for x in range(strip_len):
        strip.setPixelColor(strip_len*2-1-x,leds[x])
    strip.show()

###### MAIN ######
signal.signal(signal.SIGINT, signal_handler)
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

rise_time=(sun_rise[0]*3600+sun_rise[1]*60)
set_time=(sun_set[0]*3600+sun_set[1]*60)
strip_len=strip.numPixels()/2

while loop:
    now = datetime.datetime.time(datetime.datetime.now())
    secs=(now.hour*3600+now.minute*60+now.second)
    sky(strip, set_time, rise_time, strip_len, preshow, show)
    sun_and_moon(strip, set_time, rise_time, strip_len)
    dimmer(strip, set_time, rise_time, preshow, show)
    strip_show(strip)
    time.sleep(1)
print('Exiting')
sys.exit(0)

#take look at the mover dist
#import matplotlib.pyplot as plt
#pos, wid = 6.7, 2
#scaler=1/normpdf(pos, pos, wid)
#plt.plot([normpdf(x, pos, wid)*scaler for x in range(20)], scalex=[x for x in range(20)])