
import time
import math

from plyer import gps

from kivy.clock import mainthread

use_gps = True
gps_on = False
lat = 00
lon = 00
bearing = 0
speed = 0
accuracy = 1000

gps_scale = 5. #1 meter in GPS is 5m in game
last_update=0

def hard_reset():
    global lat, lon
    lat = 0
    lon = 0

@mainthread
def update_location(**kwargs):
    global lat, lon, bearing, scale, accuracy, last_update
    print 'lat: {lat}, lon: {lon}, accuracy:{accuracy}'.format(**kwargs)

    tc = 1 if not last_update else (time.time()-last_update)
    last_update = time.time()
    

    lat_frac = kwargs['lat']/90.

    #from http://stackoverflow.com/a/19356480
    m_per_deg_lat = gps_scale * ( 111132.954 - 559.822 * math.cos( 2 * lat_frac ) + 1.175 * math.cos( 4 * lat_frac ) )
    m_per_deg_lon = gps_scale * ( 111132.954 * math.cos ( lat_frac ) )

    bearing = kwargs['bearing']
    speed = kwargs['speed']
    accuracy = kwargs['accuracy']

    lat = ( kwargs['lat'] * m_per_deg_lat ) % 100000
    lon = ( kwargs['lon'] * m_per_deg_lon ) % 100000

@mainthread
def on_status(self, *args, **kwargs):
    print 'GPS status: ',args, kwargs

try:
    gps.configure(on_location=update_location, on_status=on_status)
except Exception as ex:
    template = "An exception of type {0} occured. Arguments: {1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message
    use_gps = False

def start():
    out = 'Dummy'
    if use_gps:
        out = gps.start(1000, 0)
        gps_on = True
    return out

def stop():
    if use_gps:
        gps.stop()
        gps_on = False

def get_location():
    import random
    global lat, lon, last_update, accuracy

    if not use_gps: #sham update method for testing on desktop
        lon += 5*tc*(random.random() ) #* gps_scale/100000
        lat += 2.5*tc*(random.random() )
        accuracy = 1

    return [lon, lat]

def get_bearing():
    return bearing

if __name__ == "__main__":
    print use_gps, get_location(), gps_on
