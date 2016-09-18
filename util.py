import logging
import numpy as np
import string
import globalvars
import uuid
import pickle
import os
import sys
import random
import math
import importlib


#TIME_FACTOR = 168 # 1 irl hour = 1 week
#TIME_FACTOR = 24 # 1 irl hour = 1 day
#TIME_FACTOR = 120

#ZOOM = 15

#GRAPHICS = None
GLOBAL_X=0
GLOBAL_Y=0


#from http://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def get_skew(skew = 'linear'):
    if skew == 'linear':
        return random.gauss(0,0.25)
    return 0

def sround(num):
    base = math.floor(num)    
    return int(base + 1) if random.random() < num%1 else int(base)       

def radian(deg):
    return 3.14159*deg/180

def degree(rad):
    return 180*rad/3.14159

def register(obj, oid=''):
    new_id = oid if oid else str(uuid.uuid4())
    try:
        globalvars.ids[new_id] = obj
        obj.id = new_id
    except:
        assert False, "global id collision!"
    return new_id

def unregister(obj):
    globalvars.ids.pop(obj.id)

def quad_mean(x,y,wx=1,wy=1):
    return pow( (1.0*wx*x*x + wy*y*y)/(wx + wy) ,0.5)
    
def timestring(seconds):
    seconds = int(seconds)
    time=''
    div, rem = (seconds/(2592000*12),seconds%(2592000*12))    
    if div: time = ''.join([time,str(div),' year ' if div==1 else ' years ' ])
    seconds = rem
    div, rem = (seconds/(2592000),seconds%(2592000))    
    if div: time = ''.join([time,str(div),' month ' if div==1 else ' months ' ])
    seconds = rem
    div, rem = (seconds/(86400),seconds%(86400))    
    if div: time = ''.join([time,str(div),' day ' if div==1 else ' days ' ])
    seconds = rem
    div, rem = (seconds/(3600),seconds%(3600))    
    if div: time = ''.join([time,str(div),' hour ' if div==1 else ' hours ' ])
    seconds = rem
    time = ''.join([time,str(seconds),' seconds' ])
    return time    
    
    
def short_timestring(seconds):
    seconds = int(seconds)
    if seconds > 2592000*12:
        return '%.2f years' % (seconds/(2592000.*12))
    if seconds > 2592000:
        return '%.2f months' % (seconds/2592000.)
    if seconds > 86400:
        return '%.2f days' % (seconds/86400.)
    if seconds > 3600:
        return '%.2f hours' % (seconds/3600.)
    return '%.2f seconds' % seconds
    
def seconds(time=1,units='minutes'):
    return time*60 if units == 'minutes' or units == 'minute' \
                                         else time*3600 if units == 'hours' or units == 'hour' \
                                         else time*86400 if units=='days' or units == 'day' \
                                         else time*2592000 if units=='months' or units == 'month' \
                                         else time*2592000*12 if units=='years' or units == 'year' \
                                         else 10    
                                         
                                         
def short_id(long_id):
    return string.upper(long_id[0:4])                                                
                                         
def vec_dist(a,b):
    diff = b-a
    return np.sqrt( np.vdot( diff , diff ) )

def fig2rgb_array(fig):
    fig.canvas.draw()
    buf = fig.canvas.tostring_rgb()
    ncols, nrows = fig.canvas.get_width_height()
    return np.fromstring(buf, dtype=np.uint8).reshape(nrows, ncols, 3)

generic_logger=logging.getLogger("SystemLog")
generic_logger.setLevel(logging.DEBUG)
#DEBUG INFO WARNING ERROR CRITICAL
#create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
#create formatter
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#add formatter to ch
ch.setFormatter(formatter)
#add ch to logger
generic_logger.addHandler(ch)

generic_logger.debug("Logger initiated.")

def autosave():
    try:
        datafile = open(os.path.join('save','autosave'),'w')
        pickle.dump(globalvars.universe,datafile,2)        
        datafile.close()
        generic_logger.info("Universe saved.  Superman given the day off.")
        return True
    except:
        e = sys.exc_info()[0]
        generic_logger.warning("Autosave failed: %s" % e)
    return False
        
    
def autoload():
    try:
        datafile = open(os.path.join('save','autosave'),'r')
        #global universe
        globalvars.universe = pickle.load(datafile)
        datafile.close()
        generic_logger.info("Universe loaded.  Initiating prime mover...")
        return True
    except:
        e = sys.exc_info()[0]
        generic_logger.warning("Autoload failed: %s" % e)
    return False
       
