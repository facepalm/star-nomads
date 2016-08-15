from kivy.clock import Clock
import time

import gps
import util
import shipimage
import shippanel
import globalvars

class Ship(object):
    def __init__(self):
        self.id = util.register(self)
        self.rooms = []        
        self.crew = 0
        if not hasattr(self, 'shipclass'): self.shipclass = 'Generic'
        if not hasattr(self, 'faction'): self.faction = 'NPC'
        
        self.location = [0, 0]
        self.bearing = 0
        
        if not hasattr(self, 'image'): self.image = shipimage.ShipImage(ship=self)
                
    def update(self,secs):
        pass
        
    def get_location(self):
        return self.location
        
    def touched(self):
        pass

class Ark(Ship): #Player ship, or potentially player ship
    def __init__(self):        
        self.style = 'Generic' #Warship Worldship Junkship     
        self.shipclass = 'Ark'
        self.faction = 'Player'  
        self.image = shipimage.ShipImage(ship=self)
        self.screen = None
        Ship.__init__(self)
        
    def get_location(self):
        self.location = gps.get_location()
        
        return gps.get_location()        
        
    def update(self,dt):
        self.location = gps.get_location()
        self.bearing = gps.get_bearing()
        self.image.coords = self.location        
        self.image.bearing = self.bearing
        
    def touched(self):
        #go to ship screen
        if self.screen is None:
            self.screen = shippanel.ShipScreen(ship=self)
        if not globalvars.root.screen_manager.has_screen(self.screen.name):
            globalvars.root.screen_manager.add_widget( self.screen )
        globalvars.root.onNextScreen(self.screen.name)
        print 'screen added'
        
        
        
class Premise(Ark): #default ship 
    def __init__(self):
        Ark.__init__(self)
        self.style = 'Premise'
        
        self.rooms = [  {'size':1, 'loc':   [0  ,0  ], 'module': None },
                        {'size':1, 'loc':   [100,0  ], 'module': None } ]
                        
                                
