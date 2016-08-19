from kivy.clock import Clock
import time
import random
#from functools import reduce

import gps
import util
import shipimage
import shippanel
import globalvars
import resources

import modules

def power_scaling(power=1):
    return 10**power

class Ship(object):
    def __init__(self):
        self.id = util.register(self)
        self.rooms = []        
        self.crew = 0
        if not hasattr(self, 'shipclass'): self.shipclass = 'Generic'
        if not hasattr(self, 'faction'): self.faction = 'NPC'
        
        self.location = [0, 0]
        self.bearing = 0
        
        self.res = resources.ResourceModel()
        
        self.active_sensors={}
        self.passive_sensors={}
        self.crew_managed = {}
        self.housing = {}
        self.power = {}
        self.power_use={}
        self.crew_use={}
        self.storage = {}
        
        self.crew = {   'Civilian'  : 0, 
                        'Trained Crew' : 0 }
        
        if not hasattr(self, 'image'): self.image = shipimage.ShipImage(ship=self)

    def has_res(self,res_name,amt):
        return self.res.has(res_name,amt)
        
    def can_hold_res(self,res_name,amt):
        if not res_name in resources.resources: return False
        stor = self.storage[resources.resources[res_name]['restype']]
        cur_amt = self.res.amount(res_name)
        return stor >= amt + cur_amt
        
    def add_res(self,res_name,amt):
        self.res.add(res_name,amt)
    
    def sub_res(self,res_name,amt):
        return self.res.sub(res_name,amt)       
                
    def update(self,secs):
        pass
        
    def get_location(self):
        return self.location
        
    def touched(self):
        pass
        
    def sensor_strength(self,active=False):
        if active: return max(self.active_sensors.values()) if self.active_sensors else 0
        return max(self.passive_sensors.values()) if self.passive_sensors else 0       
        
    def power_available(self, amt, offset = 0):
        if amt == 0: return True
        power = sum([3*power_scaling(x) for x in self.power.values() ])
        p_u = sum([power_scaling(x) for x in self.power_use.values() ])    
        return power - p_u + offset >= amt
        
    def crew_available(self, amt, offset = 0):
        crew = self.crew['Trained Crew']
        c_u = sum(self.crew_use.values())
        return crew - c_u + offset >= amt        
        
    def storage_available(self,res_type='Solid'):
        if res_type not in self.storage: return 0
        return sum(self.storage['res_type'].values())        

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
                        {'size':3, 'loc':   [0   , 125], 'module': modules.PhlebGenerator(ship=self) },
                        {'size':2, 'loc':   [0   ,  10], 'module': modules.Quarters(ship=self) },
                        {'size':2, 'loc':   [0   , 240], 'module': modules.BridgeSz2(ship=self) },
                        {'size':1, 'loc':   [110 , 170], 'module': None }, #antimatter storage
                        {'size':1, 'loc':   [-110, 170], 'module': None }, #life support
                        {'size':1, 'loc':   [-110,  75], 'module': None }, #hyperdrive core?
                        {'size':1, 'loc':   [110 ,  75], 'module': None }, #CPU core?
                        
                        #outer circle
                        {'size':1, 'loc':   [-200, 175], 'module': None }, #weapon?
                        {'size':1, 'loc':   [-150, 260], 'module': None },                         
                        {'size':1, 'loc':   [-50 , 320], 'module': modules.SensorSuite(ship=self) },
                        {'size':1, 'loc':   [50  , 320], 'module': None }, #weapon?
                        {'size':1, 'loc':   [150 , 260], 'module': modules.Storage(ship=self) }, 
                        {'size':1, 'loc':   [200 , 175], 'module': None }, #asteroid processing
                                               
                        #wings 
                        {'size':3, 'loc':   [-200,   0], 'module': None }, #dry dock
                        {'size':3, 'loc':   [200 ,   0], 'module': None },
                        {'size':2, 'loc':   [-125,-100], 'module': modules.Quarters(ship=self) },
                        {'size':2, 'loc':   [125 ,-100], 'module': None }, #trade dock
                        {'size':2, 'loc':   [-200,-250], 'module': None },
                        {'size':2, 'loc':   [ 200,-250], 'module': modules.StorageSz2(ship=self) }]

        self.crew = {   'Civilian'  : random.randint(200,600), 
                        'Trained Crew' : random.randint(200,600) }                        
                                
    def update(self,dt):
        Ark.update(self,dt)                                
        #print self.storage 
       
