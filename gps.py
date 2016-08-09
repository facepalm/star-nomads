
from plyer import gps

use_gps = True
gps_on = False
lat = 0
lon = 0

gps_scale = 100000

def update_location(**kwargs):
    print 'lat: {lat}, lon: {lon}'.format(**kwargs)
    lat = kwargs['lat'] * gps_scale
    lon = kwargs['lon'] * gps_scale

try:
    gps.configure(on_location=update_location)
except Exception as ex:
    template = "An exception of type {0} occured. Arguments: {1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message
    use_gps = False   
    
def start():  
    if use_gps:       
        gps.start(1000, 0)
        gps_on = True

def stop():
    if use_gps:
        gps.stop()
        gps_on = False
    
def get_location():
    import random
    global lat, lon
    if not use_gps: lon += (random.random() )/1 #* gps_scale/100000
    #lon += (random.random() )/10
    #if random.random() < 0.05: 
    #    print 'should trigger!'
    #    return [10,10]
    return [lat, lon]    
    
if __name__ == "__main__":
    print use_gps, get_location(), gps_on
