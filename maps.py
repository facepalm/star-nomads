import random
import numpy as np

import util
import mapscreen
import event
import asteroid
import star
import gps
import globalvars

EVENT_TC = 720.

M_TO_LY = 1000.

class Map(object): #more or less just a container for all of the things that happen in space
    def __init__(self, ship=None):
        self.id = util.register(self)
        self.mapseed = random.random()*10000
        random.seed(self.mapseed)
        
        self.events = [] #list for unpopped events - do we even need this here?
        self.objects = [] #popped events.  Mostly just little stuff like resource finds
        
        self.stars = {}
        
        self.ship = ship #convenience link to get location information
        
        self.density = int(500 / random.random()**1.25) #avg disctance between stars, where 1 km == 1 ly TODO galaxy map?
        print 'Star distance',self.density
        
        self.display = mapscreen.MapScreen(map=self)
        #self.display.add_widget(self.ship.image)
        self.event_mgr = event.EventManager()
        
        self.update_starmap()

    def update(self,secs):
        loc = None
        #if self.ship is not None:
        loc = gps.get_location()
        self.display.location = loc
        self.display.on_location()
        self.display.update(secs)
        self.update_starmap()
            #print self.systemcoord(loc)
            
        #one event every hour or so?        
        num = util.sround( random.random()*secs/EVENT_TC )
        for i in range(num):
            #new event at current location... ish
            new_event = self.event_mgr.new(loc)
            if new_event:
                #ping location
                self.display.ids['mapscale'].add_widget(new_event.mapimage)
                #self.display.spawn_ping(location=new_event.location,extent=100.,color=new_event.color)
        if random.random() < 0.1:
            self.display.event_ping(extent=self.ship.sensor_strength(active=True))                
            
        events = self.event_mgr.fetch_all(loc,self.ship.sensor_strength())
        for e in events:            
            if not e.discovered: e.discover(curmap=self)
            
    def update_starmap(self,loc=None,dist=3):
        if loc is None: loc = self.display.location
        print loc, self.systemcoord(loc)
        loc = self.systemcoord(loc)
        
        for x in np.linspace(loc[0]-dist*self.density,loc[0]+dist*self.density,num=dist*2+1):
            for y in np.linspace(loc[1]-dist*self.density,loc[1]+dist*self.density,num=dist*2+1):
                newloc = (int(round(x)),int(round(y)))
                #print newloc
                if newloc not in self.stars:
                    print 'Adding new star at',newloc
                    self.stars[newloc] = star.initialize_star(newloc,self.density,int(abs(self.mapseed+y*x+x+y)),self.display.ids['mapscale'])
                    if self.stars[newloc]: 
                        print self.stars[newloc].info()
                        #self.display.ids['mapscale'].add_widget(self.stars[newloc].primary_image())

        
    def which_system(self,loc=None):
        if loc is None: loc = self.display.location
        loc = self.systemcoord(loc)
        newloc = (int(round(loc[0])),int(round(loc[1])))  
        closest = None
        best_dist = 0
        for x in np.linspace(loc[0]-self.density,loc[0]+self.density,num=3):
            for y in np.linspace(loc[1]-self.density,loc[1]+self.density,num=3):
                newloc = (int(round(x)),int(round(y)))
                if newloc not in self.stars:
                    self.update_starmap()
                if closest is None or (self.stars[newloc] and util.vec_dist(self.stars[newloc].loc, np.array(self.display.location)) < best_dist):
                    closest = self.stars[newloc]
                    best_dist = util.vec_dist(self.stars[newloc].loc, np.array(self.display.location)) if closest else 0
        print closest.info(), best_dist / globalvars.M_TO_AU, closest.snow_line
        return closest
        
                
        
    def new_player_ship(self,ship):
        #TODO remove old ship if present?
        
        self.ship = ship       
        
        #hand to mapscreen        
        self.display.ids['mapscale'].add_widget(self.ship.image)

    def spawn(self,item,loc):
        if item=='asteroid':
            ast = asteroid.Asteroid(location=loc,curmap=self)
            
    def systemcoord(self,loc):
        nloc = self.density * (np.array(loc) // self.density)
        return nloc.round().tolist()
        
            
