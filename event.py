import util
import random

import numpy as np

class Event(object):
    def __init__(self,**kwargs):
        util.register(self)
        
        self.state = 'UNSPAWNED'
        
        self.location = kwargs['location']
        self.category = kwargs['etype'] if 'etype' in kwargs else 'Generic'
        
        
        
        self.spawn_in  = random.random() * 7200.
        self.expire_in = 3600.*24 * (1+ random.random())
        
        self.exclusion_radius = 10
        
    def update(self,secs):
        if self.spawn_in > 0:
            self.spawn_in -= secs
            if self.spawn_in < 0:
                print 'Event spawning at', self.location
                #spawn logic
        else:    
            self.expire_in -= secs
            if self.expire_in < 0:
                print 'Event expiring at', self.location
                self.state = 'EXPIRED'
                util.unregister(self) #will no longer update
            
class EventManager(object):
    jitter = 100 

    def __init__(self):
        util.register(self)
        
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
            
    def update(self,secs):
        live_events = []
        for e in self.events:
            if e.state not in ['EXPIRED','RESOLVED']:
                live_events.append(e)

        self.events = live_events                
                    
