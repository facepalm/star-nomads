import random

from kivy.lang import Builder
from kivy.uix.image import Image


import util
import globalvars

all_modules = dict()

kv = '''
<ModuleImage@Image>:
    size: '40dp','40dp'
    size_hint: None, None   
    
    Image:
        id: modsize
        source: None
          
                           
'''
Builder.load_string(kv)


class ModuleImage(Image):
    def __init__(self,**kwargs):
        self.module = kwargs['module']
        self.source = self.module.img_dict['icon']
        super(ModuleImage,self).__init__(**kwargs)
        
        #self.ids['modsize'].source = ''.join(['img/icon/modules/',str(self.module.size),'.png'])
        #self.ids['modsize'].center = self.module.img_dict['sizeloc']
        

class Module(object):
    def __init__(self,**kwargs):
        globalvars.map.register(self)
        
        self.name = 'Module'
        
        self.ship = kwargs['ship']
        self.ship.crew_use[self.id] = 0
        
        self.room = kwargs['room'] if 'room' in kwargs else None
        #super(Module, self).__init__(**kwargs)
        
        self.size = all_modules[type(self).__name__]['Size'] if type(self).__name__ in all_modules else 1
        self.power_needed = all_modules[type(self).__name__]['Power'] if type(self).__name__ in all_modules else 0
        self.crew_needed = all_modules[type(self).__name__]['Crew'] if type(self).__name__ in all_modules else 0
        
        self.crew = 0
        
        self.crewed = False
        self.active = False
        self.toggled = True 
        
        self.storage = {}
        if not hasattr(self, 'recipe'): self.recipe = []
        
        self.condition = 1.0 
        self.maint_reqr = False
        
        self.img_dict = {'icon':'img/icon/modules/blank.png', 'sizeloc': [0,0], 'statusloc':[0,0], 'displaysize':True, 'icon color':[0.8,0.8,0.8,1.0]}
        
        if not hasattr(self,'idle_activity'): self.idle_activity = {'Name':'Idle', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'hour')}
        self.activity = self.idle_activity.copy()
        self.status = 'Module Rebooting...'
        
        self.color= [0.5, 0.5, 0.5, 1.0]
        
        self.full_activity = {'Name':'Waiting for storage', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'hour')}
        
        self.image=None
        self.module_image()
        
    def module_image(self):
        if not self.image: 
            self.image = ModuleImage(module=self)
        return self.image
        
    def update(self, secs):
        timeslice = min(1.,secs/util.seconds(1, 'day'))
        
        if self.active and self.activity['Name'] != 'Idle': 
            self.color = [0.3, 0.5, 1.0, 1.0]
        elif self.crewed and not self.maint_reqr: 
            self.color = [0.4, 0.4, 0.2, 1.0]
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
           
        if self.activity['Name'] not in ['Idle','Waiting for storage'] and self.activity['Duration'] > 0:                
            self.active = True
            self.activity['Duration'] -= secs 
            self.status = 'Operational'#'Job: ' + self.activity['Name'] +' '+ str(self.activity['Duration'])
            self.ship.power_use[self.id] = self.power_needed   
            if self.activity['Duration'] <= 0: #end job
                self.finish_job()                            
        else:
            #idle
            self.status = 'Idling'      
            self.ship.power_use[self.id] = 0
            self.active = False              
          
            
        if self.active:                                
            #reduced crew have a chance for something to break
            if random.random() < 0.03 * timeslice: #TODO scale with condition - poor modules break more often
                self.maint_reqr = True    
                                                                                                                                                            
        else: #pick a new activity
            #check if we can power up
            if not self.ship.power_available(self.power_needed,offset=self.ship.power_use[self.id]):                  
                self.status = 'Idling: Low Power' 
                self.activity = self.idle_activity.copy()
                return
                    
            #check recipes
            random.shuffle(self.recipe)
            for r in self.recipe:
                
                begin = self.check_job(r)
                if begin: 
                    self.start_job(r)
                else:
                    self.activity = self.idle_activity.copy() 
                    
            if len(self.recipe ) == 0:
                self.activity = self.idle_activity.copy() 
              
            self.status = 'Ready'#self.activity['Name']

    def check_job(self,recipe):
        #check operational
        if self.maint_reqr: return False
        #check inputs
        if False in self.ship.storage.has_list(recipe['Inputs']).values(): return False
            
        #check profitability
        cost = self.ship.storage.price_list(recipe['Inputs'])
        prof = self.ship.storage.price_list(recipe['Outputs'])    
        
        if prof < cost and 'Priority' not in recipe: return False
        
        return True                       

    def start_job(self,recipe):
        #pull inputs
        for i in recipe['Inputs']:
            self.ship.sub_res(i,recipe['Inputs'][i])
        self.activity = recipe.copy()
        self.active = True                      

    def finish_job(self):
        recipe = self.activity
        #check if we can store outputs
        for i in recipe['Outputs']:
            if not self.ship.can_hold_res(i,recipe['Outputs'][i]):
                self.activity = self.full_activity.copy()
                self.activity['Outputs'] = recipe['Outputs'].copy()
        
        #push outputs
        for i in recipe['Outputs']:
            self.ship.add_res(i,recipe['Outputs'][i])
        self.activity = self.idle_activity.copy()
        self.active = False
        
    def get_room(self):
        if self.room is not None: return self.room
        find_me = [x for x in self.ship.rooms if x['Module'] is self]
        if len(find_me) > 1: assert False, 'Error: two rooms have same module'
        if len(find_me) == 0: return None
        return find_me[0]     
                       
    def on_toggle(self):
        self.toggled = False if self.toggled else True
        
    def txt_info(self):
        out = self.name + ' ' + util.short_id(self.id) + '\n'
        out += 'Status: '+self.status+'\n'
        out += 'Job: '+self.activity['Name'] + '\n'
        if self.activity['Name'] != 'Idle':
            out += 'Ready in:'+ '{0:1.2f}s \n'.format(self.activity['Duration'])
        return out


class Cabin(Module): 
    all_modules['Cabin'] = {'Name':'Cabins', 'Size':1, 'Power':0, 'Crew':10}
   
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        self.housing = 100    
        self.img_dict['icon']='img/icon/noun-project/icon54-housing-1.png'
        self.img_dict['displaysize'] = False
        
    def update(self,secs):        
        Module.update(self,secs)
        self.ship.housing[self.id] = self.housing if not self.maint_reqr else self.housing/2
             
        
class Quarters(Cabin):    
    all_modules['Quarters'] = {'Name':'Quarters', 'Size':2, 'Power':1, 'Crew':50}
    
    def __init__(self,**kwargs):
        Cabin.__init__(self,**kwargs)
        self.img_dict['icon']='img/icon/noun-project/icon54-housing-2.png'
        self.housing = 1000
        
        self.recipe = [{'Name':'Process Hydrates', 'Inputs': {'Hydrates':200}, 'Outputs': {'Water':196,'Organics':2,'Silicates':2}, 'Duration' : util.seconds(1,'hour')}]
        
class ResidentialBlock(Cabin):  

    all_modules['ResidentialBlock'] = {'Name':'Residential Block', 'Size':3, 'Power':2, 'Crew':100}
      
    def __init__(self,**kwargs):
        Cabin.__init__(self,**kwargs)
        self.img_dict['icon']='img/icon/noun-project/icon54-housing-3.png'
        self.housing = 10000
           
        
class Storage(Module):
    all_modules['Storage'] = {'Name':'Small Storage', 'Size':1, 'Power':0, 'Crew':1}

    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        
        self.storage_type = 'Basic'
        self.storage_amt = 1000
        self.img_dict['icon']='img/icon/noun-project/rockicon-box.png'
        self.img_dict['displaysize'] = False
        
    def update(self,secs):        
        Module.update(self,secs)
        if self.storage_type not in self.ship.storage_limit: self.ship.storage_limit[self.storage_type] = dict()
        self.ship.storage_limit[self.storage_type][self.id] = self.storage_amt if self.crewed else 0
        
class StorageSz2(Storage):
    all_modules['StorageSz2'] = {'Name':'Storage Area', 'Size':2, 'Power':0, 'Crew':5}
    def __init__(self,**kwargs):
        Storage.__init__(self,**kwargs)
        
        self.storage_type = 'Basic'
        self.storage_amt = 10000       
        
class StorageSz3(Storage):
    all_modules['StorageSz3'] = {'Name':'Large Storage', 'Size':3, 'Power':0, 'Crew':25}
    
    def __init__(self,**kwargs):
        Storage.__init__(self,**kwargs)        
        self.storage_type = 'Basic'
        self.storage_amt = 100000        
        
        
class Bridge(Module): #small dedicated bridge
    all_modules['Bridge'] = {'Name':'Aux. Bridge', 'Size':1, 'Power':0, 'Crew':2}
    
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        self.crew_managed = 10 
        self.passive = 10
        
        self.img_dict['icon']='img/icon/noun-project/arthur-shlain-bridge.png'
        self.img_dict['displaysize'] = False
        
    def update(self,secs):
        Module.update(self,secs)
        
        self.ship.crew_managed[self.id] = self.crew_managed
        self.ship.passive_sensors[self.id] = self.passive                    
        
class BridgeSz2(Bridge):
    all_modules['BridgeSz2'] = {'Name':'Bridge', 'Size':2, 'Power':1, 'Crew':100}
    def __init__(self,**kwargs):
        Bridge.__init__(self,**kwargs)      
        self.crew_managed = 1000
        
class BridgeSz3(Bridge):
    all_modules['BridgeSz3'] = {'Name':'Command Deck', 'Size':3, 'Power':2, 'Crew':200}
    def __init__(self,**kwargs):
        Bridge.__init__(self,**kwargs)      
        self.crew_managed = 10000        
        
        
class Reactor(Module):
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs) 
        self.power_supplied = 0
        self.img_dict['displaysize'] = False
        
    def update(self,secs):
        Module.update(self,secs)
        self.ship.power[self.id] = self.power_supplied if self.active else 0
        #print self.status
            
        
class PhlebDrive(Reactor):
    all_modules['PhlebDrive'] = {'Name':'Phlebotinum Drive', 'Size':1, 'Power':0, 'Crew':1}
    def __init__(self,**kwargs):
        Reactor.__init__(self,**kwargs) 
        self.power_supplied = 1
        self.recipe = [{'Name':'Operating', 'Inputs':{'Charged Phlebotinum': 1}, 'Outputs':{'Depleted Phlebotinum':1}, 'Duration':util.seconds(1,'day')}]
               
class PhlebCycler(Reactor):
    all_modules['PhlebCycler'] = {'Name':'Phlebotinum Cycler', 'Size':2, 'Power':0, 'Crew':5}
    def __init__(self,**kwargs):
        Reactor.__init__(self,**kwargs) 
        self.power_supplied = 2
        self.recipe =[ {'Name':'Operating', 'Inputs':{'Charged Phlebotinum': 2}, 'Outputs':{'Depleted Phlebotinum':2}, 'Duration':util.seconds(1,'day')}]
        
                

class PhlebGenerator(Reactor):
    all_modules['PhlebGenerator'] = {'Name':'Zero-point Generator', 'Size':3, 'Power':0, 'Crew':20}
    def __init__(self,**kwargs):
        Reactor.__init__(self,**kwargs) 
        self.power_supplied = 3
        self.recipe = [{'Name':'Operating', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'day')}]
        self.img_dict['icon']='img/icon/noun-project/ryan-lerch-three-prong-outlet.png'
        
        
        
        
class SensorSuite(Module):
    all_modules['SensorSuite'] = {'Name':'Active Sensors', 'Size':1, 'Power':1, 'Crew':3}
    def __init__(self,**kwargs):
        self.idle_activity = {'Name':'Beeping Noise', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'hour')}
        Module.__init__(self,**kwargs)        
        self.active_sens = 100             
        self.passive_sens = 25
        
        self.img_dict['icon']='img/icon/noun-project/andrejs-kirma-antenna.png'
        self.img_dict['displaysize'] = False
        
    def update(self,secs):
        Module.update(self,secs)        
        if self.active:
            self.ship.active_sensors[self.id] = self.active_sens
            self.ship.passive_sensors[self.id] = self.passive_sens    
        else:                     
            self.ship.active_sensors[self.id] = 0
            self.ship.passive_sensors[self.id] = 10
      
class HyperDrive(Module):
    all_modules['HyperDrive'] = {'Name':'Hyperspace Core', 'Size':1, 'Power':2, 'Crew':20}
    def __init__(self,**kwargs):
        self.recipe = [{'Name':'Charging', 'Inputs':{}, 'Outputs':{}, 'Duration':util.seconds(1,'day')}]
        Module.__init__(self,**kwargs)        
        self.charge = 0
        self.charge_rate = 0.0001
        
        self.img_dict['icon']='img/icon/noun-project/brian-oppenlander-arrows.png'
        self.img_dict['displaysize'] = False
        
    def update(self,secs):
        Module.update(self,secs)
        self.ship.hyperspace_charge[self.id] = self.charge        
        if self.active:
            self.charge += self.charge_rate * secs
            self.charge = min(1.,self.charge)
            self.activity['Duration'] = max(0,(1-self.charge)/self.charge_rate)
                
            
class SmelterSz2(Module):
    all_modules['SmelterSz2'] = {'Name':'Smelter', 'Size':1, 'Power':2, 'Crew':50}
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)
        
        self.recipe = [{'Name':'Smelt Metal', 'Inputs': {'Metallics':5000}, 'Outputs': {'Metals':2500,'Slag':2500}, 'Duration' : util.seconds(1,'hour')},
                       {'Name':'Reclaim Slag', 'Inputs': {'Slag':5000}, 'Outputs': {'Metallics':1000,'Silicates':3000,'Reactives':1000}, 'Duration' : util.seconds(1,'hour')},
                       {'Name':'Purify Silicon', 'Inputs': {'Silicates':5000, 'Carbon':1600, 'Oxygen':2133}, 'Outputs': {'Silicon':1866,'Reactives':1000,'Carbon Dioxide':5866}, 'Duration' : util.seconds(1,'hour')}]
                       
        self.img_dict['icon']='img/icon/noun-project/icon54-factory-chimney.png'
        self.img_dict['displaysize'] = False            
            
            
class GreenhouseSz1(Module):
    all_modules['GreenhouseSz1'] = {'Name':'Hydroponics', 'Size':1, 'Power':1, 'Crew':10}
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)

        self.multiplier = 1000
        
        self.recipe = [{'Name':'Grow baby grow', 'Inputs': {'Organics':1.*self.multiplier,'Water':0.9*self.multiplier,'Carbon Dioxide':1.1*self.multiplier}, 'Outputs': {'Oxygen':0.8*self.multiplier, 'Biomass':1.3*self.multiplier, 'Organics':0.9*self.multiplier}, 'Duration' : util.seconds(1,'hour')}]
                       #{'Name':'Compost Organics', 'Inputs': {'Organics':100,'Water':10}, 'Outputs': {'Fertilizer':10,'Carbon Dioxide':10}, 'Duration' : util.seconds(1,'hour')}]    
                       
        self.biomass = 0
        self.capacity = 1000
        
        self.img_dict['icon']='img/icon/noun-project/arthur-shlain-birch-leaf.png'
        self.img_dict['displaysize'] = False 
        self.img_dict['icon color'] = [0.6,1.0,0.6,1.0]         
        
    #def update(self,secs):
        #print self.activity
        #if not self.active:
        #    timeslice = min(1,secs/util.seconds(1,'day'))
        #    self.biomass *= (1- 0.1*timeslice)
    #    pass
        
    def finish_job(self):
        self.biomass += 0.01 * self.capacity #new plants
            
        #from A biological method of including mineralized human liquid and solid wastes into the mass exchange of bio-technical life support systems
        #299g/plant total mass (wheat)
        #133g/plant edible mass
        #0.128 m^2 per plant
        #70-day growth period
        
        #co2 - 5 tons of carbon per acre per year -> 18 tons of c02
        #60 tons of forest biomass per acre
        # ~1/3 biomass per year            
        # 0.000037671 biomass per hour
        
        #co2 = self.ship.sub_res('Carbon Dioxide', self.biomass*0.000037671 )
        
        Module.finish_job(self)
                              
            
class AsteroidProcessing(Module):
    all_modules['AsteroidProcessing'] = {'Name':'Exomaterial Intake', 'Size':1, 'Power':1, 'Crew':5}
    def __init__(self,**kwargs):
        Module.__init__(self,**kwargs)

        self.asteroid = None
        self.capacity = 1E6 # a million kg should be enough for anybody
        self.throughput = 25000
        
        self.recipe = [{'Name':'Processing Asteroid', 'Inputs': {}, 'Outputs': {}, 'Duration' : util.seconds(1,'hour')}]
        self.img_dict['icon']='img/icon/noun-project/rob-armes-mining-tools.png'
        self.img_dict['displaysize'] = False
        
    def update(self,secs):        
        #print self.activity, self.status
        Module.update(self,secs)        
        self.ship.asteroid_processing[self.id] = 1 if self.asteroid is None else 0

    def check_job(self,recipe):
        #print 'asteroid check',self.asteroid
        if recipe['Name'] == 'Processing Asteroid':
            if not self.asteroid: return False
        
        return Module.check_job(self,recipe)
    
    def process_asteroid(self,ast):
        if self.asteroid or self.active or not ast: return False
        
        #split off chunk of asteroid to process
        ast = ast.split(self.capacity)
        ast.leave_map()
        
        self.asteroid=ast
                
        #self.activity = self.default_activity.copy()
        return True
        
    def finish_job(self):
        if self.activity and self.activity['Name'] == 'Processing Asteroid':
            #have finished a day's worth of asteroid processing
            print 'Chunking asteroid'
            chunk = self.asteroid.split(self.throughput)
            #add chunk to ship's storage
            self.ship.storage.merge(chunk.composition)
            
            chunk.suicide()
            
            #check if asteroid is depleted
            if self.asteroid.mass() == 0:
                #kill asteroid
                self.asteroid.suicide()
                self.asteroid=None
            else:
                pass
                #self.activity = self.default_activity.copy()   
                #print 'Asteroid processing status:',self.asteroid.mass(),'kg left!' 
        print self.ship.storage.tot_amt()                
        Module.finish_job(self)                
            
        
print all_modules           
        
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
        
    
        
