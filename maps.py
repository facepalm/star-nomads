import random
import numpy as np

import util
import mapscreen
import event
import asteroid
import star
import gps


EVENT_TC = 720.

class Map(object): #more or less just a container for all of the things that happen in space
    def __init__(self, ship=None):
        self.id = util.register(self)
        self.mapseed = random.random()*10000
        random.seed(self.mapseed)
        
        self.events = [] #list for unpopped events - do we even need this here?
        self.objects = [] #popped events.  Mostly just little stuff like resource finds
        
        self.stars = {}
        
        self.ship = ship #convenience link to get location information
        
        self.density = int(500 / random.random()**1.5) #avg disctance between stars, where 1 km == 1 ly TODO galaxy map?
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
            if not e.discovered: e.discover()
            
    def update_starmap(self,loc=None,dist=3):
        if loc is None: loc = self.display.location
        loc = self.systemcoord(loc)
        for x in np.linspace(loc[0]-dist*self.density,loc[0]+dist*self.density,num=dist*2+1):
            for y in np.linspace(loc[1]-dist*self.density,loc[1]+dist*self.density,num=dist*2+1):
                newloc = (int(x),int(y))
                print newloc
                if newloc not in self.stars:
                    print 'Adding new star at',newloc
                    self.stars[newloc] = star.initialize_star(newloc,self.density,int(abs(self.mapseed+y*x+x+y)))
                    if self.stars[newloc]: 
                        print self.stars[newloc].info()
                        self.display.ids['mapscale'].add_widget(self.stars[newloc].primary_image())
        
    def new_player_ship(self,ship):
        #TODO remove old ship if present?
        
        self.ship = ship       
        
        #hand to mapscreen        
        self.display.ids['mapscale'].add_widget(self.ship.image)

    def spawn(self,item,loc):
        if item=='asteroid':
            ast = asteroid.Asteroid(location=loc,curmap=self)
            
    def systemcoord(self,loc):
        nloc = np.array(loc) // self.density
        return nloc.round().tolist()
        
            
