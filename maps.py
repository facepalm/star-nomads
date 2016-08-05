import random

import util
import mapscreen

class Map(object): #more or less just a container for all of the things that happen in space
    def __init__(self, ship=None):
        self.id = util.register(self)
        self.events = [] #list for unpopped events - do we even need this here?
        self.objects = [] #popped events.  Mostly just little stuff like resource finds
        
        self.ship = ship #convenience link to get location information
        
        self.display = mapscreen.MapScreen()
        #self.display.add_widget(self.ship.image)

    def update(self,secs):
    
        if self.ship is not None:
            loc = self.ship.get_location()
            
        #one event every hour or so?
        num = util.sround( random.random()*secs/7200. )
        
    def new_player_ship(self,ship):
        #TODO remove old ship if present?
        
        self.ship = ship       
        
        #hand to mapscreen        
        self.display.ids['mapscale'].add_widget(self.ship.image)
         

            
