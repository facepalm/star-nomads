from kivy.clock import Clock
from kivy.uix.image import Image
import time
import random
import numpy as np
import uuid
#from functools import reduce

import gps
import util
import shipimage
import shippanel
import globalvars
import resources

import modules
import asteroid
import ai
import community

def power_scaling(power=1):
    return 10**power

class Ship(object):
    def __init__(self):
        globalvars.map.register(self)
        self.rooms = []        
        self.crew = community.Community()
        if not hasattr(self, 'shipclass'): self.shipclass = 'Generic'
        if not hasattr(self, 'faction'): self.faction = 'NPC'
        
        self.registry = {}

        if not hasattr(self, 'ai'): self.ai = ai.AI(self)
        
        self.location = [0, 0]
        self.bearing = 0
        
        self.storage = resources.ResourceModel()
        
        self.player_ship = False
        
        self.active_sensors={}
        self.passive_sensors={}
        self.crew_managed = {}
        self.housing = {}
        self.power = {}
        self.power_use={}
        self.crew_use={}
        self.storage_limit = {}
        self.asteroid_processing = {}
        self.hyperspace_charge = {}
        
        '''self.crew = {   'Civilian'  : 0, 
                        'Trained Crew' : 0 }'''
        
        if not hasattr(self, 'image'): self.image = shipimage.ShipImage(ship=self)

    def __getstate__(self):
        odict = self.__dict__.copy() # copy the dict since we change it
        del odict['image']              # remove gui entry
        if 'screen' in odict: del odict['screen']
        return odict
    
    def __setstate__(self,state):
        self.__dict__.update(state)   # update attributes
        self.image = shipimage.ShipImage(ship=self)

    def has_res(self,res_name,amt):
        return self.storage.has(res_name,amt)
        
    def can_hold_res(self,res_name,amt):
        if not res_name in resources.resources: return False
        stor = self.storage_limit[resources.resources[res_name]['restype']]
        cur_amt = self.storage.amount(res_name)
        return stor >= amt + cur_amt
        
    def add_res(self,res_name,amt):
        self.storage.add(res_name,amt)
    
    def sub_res(self,res_name,amt):
        return self.storage.sub(res_name,amt)       
        
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
        crew = self.crew.trained_crew() 
        c_u = sum(self.crew_use.values())
        return crew - c_u + offset >= amt        
        
    def storage_available(self,res_type='Solid'):
        if res_type not in self.storage: return 0
        return sum(self.storage_limit['res_type'].values())      
        
    def find_room(self,_id):
        for r in self.rooms:
            room = r['module']
            if room is not None and (room.id == _id or util.short_id(room.id) == _id): return room
        return None            
        
    def harvest(self,item):
        if not hasattr(item,'identity'): return False
        dist = util.vec_dist(self.location,item.loc)
        if dist > self.sensor_strength():
            print 'too far away!',dist
            return False, 'Harvestable object is too far away!'
        if item.identity == 'asteroid': 
            #search for free asteroid harvesting module
            for r in self.asteroid_processing:
                if self.asteroid_processing[r] > 0:
                    #load 'er up
                    room = self.find_room(r)
                    test = room.process_asteroid(item)
                    print test
                    if test: return True, 'Asteroid harvested!'
                
        print item.identity
        return False, 'Uknown item!'
      
    def register(self, obj, oid=''):
        new_id = oid if oid else str(uuid.uuid4())
        try:
            self.registry[new_id] = obj
            obj.id = new_id
        except:
            assert False, "global id collision!"
        return new_id

    def unregister(self, obj):
        if obj.id in self.registry:
            self.registry.pop(obj.id)    
        
    def update(self,secs):
        timeslice = secs/util.seconds(1,'day')
        total_crew = self.crew.population()#sum(self.crew.values())
        if total_crew > 0:                        
            food_use = self.sub_res('Biomass', 2* 0.62 * total_crew * timeslice)
            food_use /= 2.
            water_use = self.sub_res('Water',3.52 * total_crew * timeslice)
            o2_use = self.sub_res('Oxygen', 0.794 * total_crew * timeslice)
            
            co2_out = o2_use/32. * 44.  #(o2 -> co2)
            self.add_res('Carbon Dioxide',co2_out)
            self.add_res('Hydrates',water_use)
            self.add_res('Organics',food_use/3)
            self.add_res('Organics',food_use) #waste biomass from food preparation
            
            
            #self.needs['Food']=Need('Food', self, 0.62, 0.62/86400.0, 0.62/1800.0, self.new_dinner_task, self.hunger_hit,severity='HUMAN_BIOLOGICAL')
            #self.needs['Water']=Need('Water', self, 3.52, 3.52/86400.0, 3.52/600.0, self.new_drink_task, self.dehydration_hit,severity='HUMAN_BIOLOGICAL')
            #self.needs['WasteCapacitySolid']=Need('WasteCapacitySolid', self, 0.22, 0.22/192800.0, 0.22/300.0, self.number_2_task, self.code_brown)
            #self.needs['WasteCapacityLiquid']=Need('WasteCapacityLiquid', self, 3.87, 0.9675/21600.0, 3.87/30.0, self.number_1_task, self.code_yellow)  
            
        for obj in self.registry.values():
            if hasattr(obj,'update'):
                obj.update(secs)            
        

class Ark(Ship): #Player ship, or potentially player ship
    def __init__(self):        
        self.style = 'Generic' #Warship Worldship Junkship     
        self.shipclass = 'Ark'
        self.faction = 'Player'  
        Ship.__init__(self)
        self.image = shipimage.ShipImage(ship=self)
        self.screen = None
        
        self.player_ship = True
        
    def get_location(self):
        #self.location = gps.get_location()
        
        return [self.location[0],self.location[1]]
        
    def update(self,dt):
        Ship.update(self,dt)
        #we're moving to destination point
        loc = np.array(self.location)
        dest = np.array(gps.get_location())
        dist = util.vec_dist(loc,dest)
        if dist > 100000: #100km, just warp
            self.location=dest.tolist()
            self.bearing=0
        else:    
            #get speed
            
            if self.player_ship:
                speed = dist 
            else:
                speed = 0.1 * dt # m/s
            frac = min(1., speed / dist )
            
            
            
            self.location = (frac*dest + (1-frac)*loc).tolist()#gps.get_location()
            dl = dest-loc      
            self.bearing = 90-int(np.arctan2(dl[1],dl[0])*180/3.14159) #gps.get_bearing()
            #print frac, loc, dest, self.bearing
        self.image.bearing = self.bearing
        self.image.coords = self.location        
        
        
        #globalvars.universe.map.display.ids['mapscale'].add_widget(Image(size_hint=(None, None),size=(1,1),pos=self.location,color=[1,0,0,1]))
        
    def touched(self):
        #go to ship screen
        if not hasattr(self,'screen') or self.screen is None:
            self.screen = shippanel.ShipScreen(ship=self)
        globalvars.root.switchScreen(self.screen)
        print 'screen added'
        
        
        
class Premise(Ark): #default ship 
    def __init__(self):
        Ark.__init__(self)
        self.style = 'Premise'
        
        self.rooms = [  #inner hub 
                        {'size':3, 'power':1, 'loc':   [0   , 125], 'module': modules.PhlebGenerator(ship=self) },
                        {'size':2, 'power':1, 'loc':   [0   ,  10], 'module': modules.Quarters(ship=self) },
                        {'size':2, 'power':1, 'loc':   [0   , 240], 'module': modules.BridgeSz2(ship=self) },
                        {'size':1, 'power':1, 'loc':   [110 , 170], 'module': None }, #antimatter storage
                        {'size':1, 'power':1, 'loc':   [-110, 170], 'module': modules.GreenhouseSz1(ship=self) }, #life support (greenhouse)
                        {'size':1, 'power':1, 'loc':   [-110,  75], 'module': modules.HyperDrive(ship=self) }, #hyperdrive core?
                        {'size':1, 'power':1, 'loc':   [110 ,  75], 'module': None }, #research lab
                        
                        #outer circle
                        {'size':1, 'power':1, 'loc':   [-200, 175], 'module': None }, #weapon?
                        {'size':1, 'power':1, 'loc':   [-150, 260], 'module': None }, #xeno bay                        
                        {'size':1, 'power':1, 'loc':   [-50 , 320], 'module': modules.SensorSuite(ship=self) },
                        {'size':1, 'power':1, 'loc':   [50  , 320], 'module': None }, #weapon?
                        {'size':1, 'power':1, 'loc':   [150 , 260], 'module': modules.Storage(ship=self) }, 
                        {'size':1, 'power':1, 'loc':   [200 , 175], 'module': modules.AsteroidProcessing(ship=self) },
                                               
                        #wings 
                        {'size':3, 'power':3, 'loc':   [-200,   0], 'module': None }, #dry dock
                        {'size':3, 'power':3, 'loc':   [200 ,   0], 'module': None }, #nano factory
                        {'size':2, 'power':1, 'loc':   [-125,-100], 'module': modules.StorageSz2(ship=self) },
                        {'size':2, 'power':1, 'loc':   [125 ,-100], 'module': None }, #trade dock
                        {'size':2, 'power':2, 'loc':   [-200,-250], 'module': None }, #impulse drive
                        {'size':2, 'power':2, 'loc':   [ 200,-250], 'module': modules.SmelterSz2(ship=self) }] #foundry

        self.crew.spawn_pop(2000)
                                
        self.add_res('Biomass',50000)
        self.add_res('Water',10000)
        self.add_res('Oxygen',10000)                                
        self.add_res('Carbon Dioxide',10000)  
                                
    def update(self,dt):
        Ark.update(self,dt)                                
        #print self.storage 
       
