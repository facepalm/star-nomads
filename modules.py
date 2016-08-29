import random

from kivy.lang import Builder
from kivy.uix.image import Image

import util


kv = '''
<ModuleImage@Image>:
    size: '40dp','40dp'
    size_hint: None, None   
    
    Image:
        id: modsize
        source: None
          
                           
'''

class ModuleImage(Image):
    def __init__(self,**kwargs):
        self.module = kwargs['module']
        self.source = self.module.img_dict['icon']
        super(ModuleImage,self).__init__(**kwargs)
        
        #self.ids['modsize'].source = ''.join(['img/icon/modules/',str(self.module.size),'.png'])
        #self.ids['modsize'].center = self.module.img_dict['sizeloc']

class Module(object):
    def __init__(self,**kwargs):
        util.register(self)
        
        self.ship = kwargs['ship']
        self.ship.crew_use[self.id] = 0
        #super(Module, self).__init__(**kwargs)
        
        self.size = 1
        self.power_needed = 0
        self.crew_needed = 0
        
        self.crew = 0
        
        self.crewed = False
        self.active = False
        self.toggled = True 
        
        self.storage = {}
        self.recipe = []
        
        self.condition = 1.0 
        self.maint_reqr = False
        
        self.img_dict = {'icon':'img/icon/modules/filled-generic.png', 'sizeloc': [0,0], 'statusloc':[0,0]}
        
        if not hasattr(self,'idle_activity'): self.idle_activity = {'Name':'Idle', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'day')}
        self.activity = self.idle_activity.copy()
        self.status = 'Module Rebooting...'
        
        self.color= [0.5, 0.5, 0.5, 1.0]
        
    def module_image(self):
        return ModuleImage(module=self)
        
    def update(self, secs):
        timeslice = min(1.,secs/util.seconds(1, 'day'))
        
        if self.active and self.activity['Name'] != 'Idle': 
            self.color = [0.3, 0.5, 1.0, 1.0]
        elif self.crewed and not self.maint_reqr: 
            self.color = [0.2, 0.2, 0.6, 1.0]
        elif self.maint_reqr: 
            self.color = [1.0, 0.5, 0.2, 1.0]
        else:
            self.color= [0.5, 0.5, 0.5, 1.0]
        
        self.active = False            
        self.ship.power_use[self.id] = 0
                    
        if not self.toggled:
            self.status = 'Mothballed'
            return 
        
        #print self.crew_needed, self.ship.crew_use[self.id], self.ship.crew_available(3, 0)
        if self.ship.crew_available(self.crew_needed, offset=self.ship.crew_use[self.id]):  
            self.ship.crew_use[self.id] = self.crew_needed
            self.crewed = True
        else:
            self.ship.crew_use[self.id] = 0
            self.crewed = False
        
        #check repair
        if self.maint_reqr:
            #crew have a chance to repair
            if self.crewed and random.random() < timeslice: #TODO scale with condition - crappy modules take longer to repair
                self.maint_reqr = False                          
            
        if self.maint_reqr:
            self.status = 'Offline: Maint'
            return            
            
        if not self.crewed:
            self.status = 'Idling: Need Crew' 
            return                                                      
            
        if self.activity['Duration'] > 0:
            self.active = True
            self.activity['Duration'] -= secs 
            self.status = 'Job: ' + self.activity['Name'] +' '+ str(self.activity['Duration'])
            self.ship.power_use[self.id] = self.power_needed   
        else:
            pass
            #end job
        if self.activity['Name'] == 'Idle' or self.activity['Duration'] < 0:
            self.status = 'Idling'      
            self.ship.power_use[self.id] = 0   
            
        if self.active:                                
            #reduced crew have a chance for something to break
            if random.random() < 0.03 * timeslice: #TODO scale with condition - poor modules break more often
                self.maint_reqr = True    
                                                                                                                                                            
        else: #pick a new activity
            #check if we can power up
            if not self.ship.power_available(self.power_needed,offset=self.ship.power_use[self.id]):                  
                self.status = 'Idling: Low Power' 
                self.activity = {'Name':'Idle', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'day')}
                return
                    
            #check recipes
            random.shuffle(self.recipe)
            for r in self.recipe:
                pass
                
                #check if we have input
                #check if we can store output
                #do it

            self.activity = self.idle_activity.copy()                
            self.status = 'Job: ' + self.activity['Name']

    def inputs(self):
        return 0
        
    def outputs(self):
        return 1   
        
    

class Cabin(Module):    
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        self.housing = 10
        self.crew_needed = 1        
        
    def update(self,secs):        
        Module.update(self,secs)
        self.ship.housing[self.id] = self.housing if not self.maint_reqr else self.housing/2
             
        
class Quarters(Cabin):    
    def __init__(self,**kwargs):
        Cabin.__init__(self,**kwargs)
        self.housing = 1000
        self.crew_needed = 50
        self.size = 2 
        self.power_needed = 1
        
class ResidentialBlock(Cabin):    
    def __init__(self,**kwargs):
        Cabin.__init__(self,**kwargs)
        self.housing = 10000
        self.crew_needed = 100
        self.size = 3 
        self.power_needed = 2
        
          
                                
        
class Storage(Module):
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        
        self.storage_type = 'Basic'
        self.storage_amt = 1000
        self.crew_needed = 1
        
    def update(self,secs):        
        Module.update(self,secs)
        if self.storage_type not in self.ship.storage: self.ship.storage[self.storage_type] = dict()
        self.ship.storage[self.storage_type][self.id] = self.storage_amt if self.crewed else 0
        
class StorageSz2(Storage):
    def __init__(self,**kwargs):
        Storage.__init__(self,**kwargs)
        
        self.storage_type = 'Basic'
        self.storage_amt = 10000       
        self.crew_needed = 5 
        
class StorageSz3(Storage):
    def __init__(self,**kwargs):
        Storage.__init__(self,**kwargs)
        
        self.storage_type = 'Basic'
        self.storage_amt = 100000  
        self.crew_needed = 25        
        
        
class Bridge(Module): #small dedicated bridge
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        self.size = 1
        self.crew_managed = 10
        self.crew_needed = 2  
        self.passive = 10
        
    def update(self,secs):
        Module.update(self,secs)
        
        self.ship.crew_managed[self.id] = self.crew_managed
        self.ship.passive_sensors[self.id] = self.passive                    
        
class BridgeSz2(Bridge):
    def __init__(self,**kwargs):
        Bridge.__init__(self,**kwargs)
        
        self.size = 2                    
        self.power_needed = 1
        self.crew_needed = 100        
        self.crew_managed = 1000
        
class BridgeSz3(Bridge):
    def __init__(self,**kwargs):
        Bridge.__init__(self,**kwargs)
        
        self.size = 3                    
        self.power_needed = 2
        self.crew_needed = 200        
        self.crew_managed = 10000        
        
        
class Reactor(Module):
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs) 
        self.power_supplied = 0
        
    def update(self,secs):
        Module.update(self,secs)
        self.ship.power[self.id] = self.power_supplied if self.active else 0
        #print self.status
            
        
class PhlebDrive(Reactor):
    def __init__(self,**kwargs):
        Reactor.__init__(self,**kwargs) 
        self.power_supplied = 1
        self.crew_needed = 1
        self.idle_activity = {'Name':'Operating', 'Inputs':{'Charged Phlebotinum': 1}, 'Outputs':{'Depleted Phlebotinum':1}, 'Duration':util.seconds(1,'day')}
               
class PhlebCycler(Reactor):
    def __init__(self,**kwargs):
        self.idle_activity = {'Name':'Operating', 'Inputs':{'Charged Phlebotinum': 2}, 'Outputs':{'Depleted Phlebotinum':2}, 'Duration':util.seconds(1,'day')}
        Reactor.__init__(self,**kwargs) 
        self.power_supplied = 2
        self.crew_needed = 5
        self.size = 2
                

class PhlebGenerator(Reactor):
    def __init__(self,**kwargs):
        Reactor.__init__(self,**kwargs) 
        self.power_supplied = 3
        self.crew_needed = 20
        self.size = 3
        self.idle_activity = {'Name':'Operating', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'day')}
        
        
        
class SensorSuite(Module):
    def __init__(self,**kwargs):
        self.idle_activity = {'Name':'Beeping Noise', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'hour')}
        Module.__init__(self,**kwargs)        
        self.active_sens = 100             
        self.passive_sens = 25
        
        self.crew_needed = 3
        self.power_needed = 1
        
    def update(self,secs):
        Module.update(self,secs)        
        if self.active:
            self.ship.active_sensors[self.id] = self.active_sens
            self.ship.passive_sensors[self.id] = self.passive_sens    
        else:                     
            self.ship.active_sensors[self.id] = 0
            self.ship.passive_sensors[self.id] = 10
            
            
class AsteroidProcessing(Module):
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        
        self.power_needed = 1
        self.crew_needed = 5
        self.asteroid = None
        
    def update(self,secs):        
        Module.update(self,secs)        
        self.ship.asteroid_processing[self.id] = 0 if self.active else 1

    def process_asteroid(self,ast):
        if self.asteroid or self.active or not ast: return False
        self.activity = {'Name':'Processing Material', 'Inputs':{}, 'Outputs':ast.components, 'Duration' : ast.size()*util.seconds(1,'hour')}
        return True
            
        
def maintenance_descriptor(maint=0.5):
    if maint > 0.9:
        return 'Pristine'
    elif maint > 0.75:
        return 'Excellent'
    elif maint > 0.6:
        return 'Good'
    elif maint > 0.5:
        return 'Fair'
    elif maint > 0.4:
        return 'Worn'
    elif maint > 0.25:
        return 'Shoddy'
    elif maint > 0.1:
        return 'Terrible'
    return 'Broken'        
        
    
        
