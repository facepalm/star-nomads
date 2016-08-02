from kivy.clock import Clock
import time

import gps
import util

class Ship(object):
    def __init__(self):
        self.id = util.register(self)
        self.rooms = []        
        self.crew = 0
        
        self.location = [0, 0]
                
    def update(self,secs):
        pass
        
    def get_location(self):
        return self.location

class Ark(Ship): #Player ship, or potentially player ship
    def __init__(self):
        Ship.__init__(self)
        self.style = 'Generic' #Warship Worldship Junkship       
        
    def get_location(self):
        return gps.get_location()        
        
class Premise(Ark): #default ship 
    def __init__(self):
        Ark.__init__(self)
        self.style = 'Premise'
        
        self.rooms = [  {'size':1, 'loc':   [0  ,0  ], 'module': None },
                        {'size':1, 'loc':   [100,0  ], 'module': None } ]
                        
                                
