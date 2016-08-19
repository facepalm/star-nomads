import util
import random

import numpy as np

import eventpanel

class Event(object):
    def __init__(self,**kwargs):
        util.register(self)
        
        self.state = 'UNSPAWNED'
        
        self.location = kwargs['location']
        self.category = kwargs['etype'] if 'etype' in kwargs else 'generic'
        
        self.color = [0.5,0.5,1.,1.]       
        
        self.discovered = False
        
        self.spawn_in  = random.random() * 7200.
        self.expire_in = 3600.*24 * (1+ random.random())
        
        self.exclusion_radius = 50
        
        self.mapimage = eventpanel.EventMapImage(event=self)
        
    def update(self,secs):
        if self.spawn_in > 0:
            self.spawn_in -= secs
            if self.spawn_in < 0:
                print 'Event spawning at', self.location
                #spawn logic
                self.state = 'SPAWNED'
        else:    
            self.expire_in -= secs
            if self.expire_in < 0:
                print 'Event expiring at', self.location
                self.state = 'EXPIRED'
                util.unregister(self) #will no longer update
                
    def discover(self,curmap=None):
        self.discovered = True        
        self.mapimage.opacity = 1        
        if self.category == 'asteroid':
            #spawn asteroid
            if curmap:
                curmap.spawn('asteroid',self.loc)
            self.state='RESOLVED'
            self.suicide()
            
        
    def on_pressed(self): #the player has touched us
        print "Event triggered!"
        if self.category == 'generic':
            self.state='RESOLVED'
            self.suicide()
        
    def suicide(self):
        util.unregister(self) #will no longer update        
        self.mapimage.suicide()
            
class EventManager(object):
    jitter = 100 

    def __init__(self):
        util.register(self)
        
        self.events = []
        
    def new(self,loc):
        if loc is None: return
        
        #pick event type
        e_type = random.choice(['generic','asteroid'])
        
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
            
            return e
        return None                        
            
    def update(self,secs):
        live_events = []
        for e in self.events:
            if e.state not in ['EXPIRED','RESOLVED']:
                live_events.append(e)

        self.events = live_events                
                    
    def fetch_all(self,location,distance=100,active_only=True):
        out = []
        location = np.array(location)
        for e in self.events:
            print  util.vec_dist(location,e.location), e.state
            if util.vec_dist(location,e.location) < distance:
                if not active_only or e.state not in ['EXPIRED','RESOLVED','UNSPAWNED']:
                    out.append(e)
        return out         
        
    def fetch_nearest(self,location,distance=100,active_only=True):
        events = self.fetch_all(location,distance,active_only)
        out = None
        for e in events:
            if not out or util.vec_dist(np.array(location),e.location) < util.vec_dist(np.array(location),out.location):
                out = e
        return out                
            
                    
