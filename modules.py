import random

import util



class Module(object):
    def __init__(self,**kwargs):
        util.register(self)
        
        self.ship = kwargs['ship']
        #super(Module, self).__init__(**kwargs)
        
        self.size = 1
        self.power_needed = 0
        self.crew_needed = 0
        
        self.crew = 0
        self.powered = False
        
        self.active = False
        self.toggled = True 
        
        self.storage = {}
        self.recipe = []
        
        self.condition = 1.0 
        self.maint_reqr = False
        
        self.always_on = False #used for modules providing a continuous service, rather than running some kind of processing
        
        self.activity = {'Name':'Idle', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'day')}
        self.status = ''
        
    def update(self, secs):
        timeslice = min(1.,secs/util.seconds(1, 'day'))
        #check repair
        if self.maint_reqr:
            #crew have a chance to repair
            if random.random() < timeslice * (self.crew + 1) / float(1 + self.crew_needed):
                self.maint_reqr = False
                
        if not self.toggled:
            self.active = False
            self.status = 'Mothballed'
            return   
            
        if self.maint_reqr:
            self.active = False
            self.status = 'Offline: Maint'
            return                                                    
            
        if self.activity['Duration'] > 0:
            self.active = True
            self.activity['Duration'] -= secs 
            self.status = 'Job: ' + self.activity['Name']
        else:
            pass
            #end job
        if self.activity['Name'] is 'Idle' or self.activity['Duration'] < 0:
            self.active = False      
            self.status = 'Idling'         
                    
            
        if self.active:                      
            #reduced crew have a chance for something to break
            if self.powered and self.crew < self.crew_needed / 2 and random.random() < 0.05 * timeslice:
                self.maint_reqr = True                                                        
                       
        if not self.active and self.crew >= self.crew_needed / 2:
                        
            #check recipes
            for r in self.recipe:
                pass
                #check if we have input
                #check if we can store output
                #do it
                


class Cabin(Module):    
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        self.housing = 10
        self.crew_needed = 1        
        self.always_on = True #quarters never really turns off 
        
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
        
        
        
        
class SensorSuite(Module):
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)        
        self.active = 100             
        self.passive = 25
        
        self.crew_needed = 3
        self.power_needed = 1
        
    def update(self,secs):
        Module.update(self,secs)
        
        self.ship.active_sensors[self.id] = self.active
        self.ship.passive_sensors[self.id] = self.passive             
        
        
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
        
    
        
