import util
import random

import numpy as np

class Event(object):
    def __init__(self,**kwargs):
        self.id = util.register(self)
        
        self.location = kwargs['location']
        
        self.scan_strength = 1 
        self.current_scan = 0
        
        self.timeout = 3600.
        
        self.exclusion_radius = 10
        
    def update(self,secs):
        self.timeout -= secs
            
class EventManager(object):
    jitter = 100 

    def __init__(self):
        self.id = util.register(self)
        
        self.events = []
        
    def new(self,loc):
        if loc is None: return
        
        #pick event type
        e_type = 'Generic'
        
        #pick event location
        offset = np.array([(random.random()-0.5)*self.jitter,(random.random()-0.5)*self.jitter])
        newloc = np.array(loc) + offset
                
        #check if event is allowed at location
        allowed = True
        for e in self.events:
            if util.vec_dist(newloc,e.location) < e.exclusion_radius:
                allowed = False
                break
        
        if allowed:
            #spawn
            print 'New event of type',e_type,' at',newloc
            e = Event(etype=e_type, location=newloc)
            self.events.append(e)
                    
