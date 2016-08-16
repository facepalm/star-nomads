import random

import util



class Module(object):
    def __init__(self,**kwargs):
        util.register(self)
        
        self.ship = kwargs['ship']
        #super(Module, self).__init__(**kwargs)
        
        self.size = 1
        self.power_draw = 0
        self.crew_needed = 0
        
        self.crew = 0
        self.powered = False
        
        self.active = False
        self.toggled = True 
        
        self.storage = {}
        self.recipe = []
        
        self.condition = 1.0 
        self.maint_reqr = False
        
    def update(self, secs):
        timeslice = secs/util.seconds(1, 'day')
        #check repair
        if self.maint_reqr:
            #crew have a chance to repair
            if random.random() * timeslice > 1 - self.crew / float(self.crew_needed):
                self.maint_reqr = False
    
        if self.toggled and self.crew >= self.crew_needed / 2 and not self.maint_reqr:
                        
            #check recipes
            for r in self.recipe:
                pass
                #check if we have input
                #check if we can store output
                #do it
                
                        
        
class Storage(Module):
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        
        
        
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
        
    
        
