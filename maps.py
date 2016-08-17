import random

import util
import mapscreen
import event

EVENT_TC = 720.

class Map(object): #more or less just a container for all of the things that happen in space
    def __init__(self, ship=None):
        self.id = util.register(self)
        self.events = [] #list for unpopped events - do we even need this here?
        self.objects = [] #popped events.  Mostly just little stuff like resource finds
        
        self.ship = ship #convenience link to get location information
        
        self.display = mapscreen.MapScreen(map=self)
        #self.display.add_widget(self.ship.image)
        self.event_mgr = event.EventManager()

    def update(self,secs):
        loc = None
        if self.ship is not None:
            loc = self.ship.get_location()
            self.display.location = loc
            
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
            
        
    def new_player_ship(self,ship):
        #TODO remove old ship if present?
        
        self.ship = ship       
        
        #hand to mapscreen        
        self.display.ids['mapscale'].add_widget(self.ship.image)
         

            
