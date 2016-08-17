from kivy.clock import Clock
import time

import gps
import util
import shipimage
import shippanel
import globalvars

import modules

class Ship(object):
    def __init__(self):
        self.id = util.register(self)
        self.rooms = []        
        self.crew = 0
        if not hasattr(self, 'shipclass'): self.shipclass = 'Generic'
        if not hasattr(self, 'faction'): self.faction = 'NPC'
        
        self.location = [0, 0]
        self.bearing = 0
        
        self.active_sensors={}
        self.passive_sensors={}
        self.crew_managed = {}
        self.housing = {}
        
        self.crew = {   'Civilian'  : 0, 
                        'Trained Crew' : 0 }
        
        if not hasattr(self, 'image'): self.image = shipimage.ShipImage(ship=self)
                
    def update(self,secs):
        pass
        
    def get_location(self):
        return self.location
        
    def touched(self):
        pass
        
    def sensor_strength(self,active=False):
        if active: return max(self.active_sensors.values()) if self.active_sensors else 0
        return max(self.passive_sensors.values()) if self.passive_sensors else 0       

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
        globalvars.root.switchScreen(self.screen)
        print 'screen added'
        
        
        
class Premise(Ark): #default ship 
    def __init__(self):
        Ark.__init__(self)
        self.style = 'Premise'
        
        self.rooms = [  #inner hub 
                        {'size':3, 'loc':   [0   , 125], 'module': None },
                        {'size':2, 'loc':   [0   ,  10], 'module': None },
                        {'size':2, 'loc':   [0   , 240], 'module': None },
                        {'size':1, 'loc':   [110 , 170], 'module': None },
                        {'size':1, 'loc':   [-110, 170], 'module': None },
                        {'size':1, 'loc':   [-110,  75], 'module': None },
                        {'size':1, 'loc':   [110 ,  75], 'module': None },
                        
                        #outer circle
                        {'size':1, 'loc':   [-200, 175], 'module': None },
                        {'size':1, 'loc':   [-150, 260], 'module': None },                         
                        {'size':1, 'loc':   [-50 , 320], 'module': modules.SensorSuite(ship=self) },
                        {'size':1, 'loc':   [50  , 320], 'module': None },
                        {'size':1, 'loc':   [150 , 260], 'module': None }, 
                        {'size':1, 'loc':   [200 , 175], 'module': None },
                                               
                        #wings 
                        {'size':3, 'loc':   [-200,   0], 'module': None },
                        {'size':3, 'loc':   [200 ,   0], 'module': None },
                        {'size':2, 'loc':   [-125,-100], 'module': None },
                        {'size':2, 'loc':   [125 ,-100], 'module': None },
                        {'size':2, 'loc':   [-200,-250], 'module': None },
                        {'size':2, 'loc':   [ 200,-250], 'module': None }]
                        
                                
