from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.core.window import Window

import math
import numpy as np
import random

import util
import globalvars


resources = {
                #tier 0
                'Ore' : {'name':'Unrefined Ore', 'restype':'Basic', 'baseval':10},
                'Crystal' : {'name':'Crystallines', 'restype':'Basic', 'baseval':10},
                'Exotic' : {'name':'Exotic Materials', 'restype':'Basic', 'baseval':1000},
                
                
                #Tier 1:
                'Duralloy' : {'name':'Duralloy', 'restype':'Basic', 'baseval':30},  #- ore heavy, crystal light, power medium
                'Phlogiston' : {'name':'Phlogiston', 'restype':'Basic', 'baseval':35}, #- ore medium, crystal medium, power heavy
                'Nanochips' : {'name':'Nanochips', 'restype':'Basic', 'baseval':30}, #- ore light, crystal heavy, power light

                #Tier 2: (mostly salvage-only)
                'RawPhleb' : {'name':'Unapplied Phlebotinum', 'restype':'Basic', 'baseval':2000}, #- exotics + crystal + phlogiston
                'Computronium' : {'name':'Reserve Computronium', 'restype':'Basic', 'baseval':2000}, #- exotics + ore + nanochips
                'Unobtanium' : {'name':'Obtained Unobtanium', 'restype':'Basic', 'baseval':2000}, #- exotics + phlogiston + duralloy 
                            
                            

                'Slag': {'name':'Slag', 'restype':'Basic', 'baseval':5}, #crap tier, rejects from other process that need processing just to be raw again
                'Waste': {'name':'Waste', 'restype':'Basic', 'baseval':5},    
        
                'Metallics': {'name':'Metallics', 'restype':'Basic', 'baseval':10}, #raw resource tier
                'Hydrates': {'name':'Hydrates', 'restype':'Basic', 'baseval':10},
                'Silicates': {'name':'Silicates', 'restype':'Basic', 'baseval':10},
                'Organics': {'name':'Organics', 'restype':'Basic', 'baseval':10},                
                'Reactives': {'name':'Reactives', 'restype':'Basic', 'baseval':10}, 
                
                'Metals': {'name':'Metals', 'restype':'Basic', 'baseval':35}, #foundry
                'Water': {'name':'Water', 'restype':'Basic', 'baseval':20}, #habitats
                'Silicon': {'name':'Silicon', 'restype':'Basic', 'baseval':20}, #foundry
                'Carbon': {'name':'Carbon', 'restype':'Basic', 'baseval':20}, #chem lab      
                'Compounds': {'name':'Compounds', 'restype':'Basic', 'baseval':20}, #chem lab
                
                'Parts': {'name':'Parts', 'restype':'Basic', 'baseval':40}, #foundry
                'Biomass': {'name':'Biomass', 'restype':'Basic', 'baseval':40}, #greenhouse
                'Silicon Wafers': {'name':'Silicon Wafers', 'restype':'Basic', 'baseval':40}, #crystal fac
                'Carbon Fiber': {'name':'Carbon Fiber', 'restype':'Basic', 'baseval':40}, #deposition fac
                'Polymers': {'name':'Polymers', 'restype':'Basic', 'baseval':40}, #chem lab
                
                'Components':{'name':'Components', 'restype':'Basic', 'baseval':80}, #additive manufacturing               
                'Electronics':{'name':'Electronics', 'restype':'Basic', 'baseval':80}, #additive manuffac                
                'Microchips':{'name':'Microchips', 'restype':'Basic', 'baseval':80}, #deposition fac    
                          
                'Computronium':{'name':'Computronium', 'restype':'Basic', 'baseval':80},
                
                'Oxygen': {'name':'Oxygen', 'restype':'Basic', 'baseval':40}, #habitats
                'Carbon Dioxide': {'name':'Carbon Dioxide', 'restype':'Basic', 'baseval':40}, #people
                
                'DeplPhleb': {'name':'Depleted Phlebotinum', 'restype':'Basic', 'baseval':10e6}, #exotics tier
                'ChrgPhleb': {'name':'Charged Phlebotinum', 'restype':'Basic', 'baseval':20e6},
            }

kv = '''
<ResourceScreen@Screen>:
    name: 'res screen'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}               
    ScrollView:
        id: resscroll               
        pos_hint: {'center_x': .5, 'center_y': .5}      
        GridLayout:
            id: resgrid
            cols:4
            spacing:10
            
            
'''

Builder.load_string(kv)

class ResourceScreen(Screen):
    changed     = BooleanProperty(False)
    visible     = BooleanProperty(False)
    
    def __init__(self,**kwargs):
        self.res = kwargs['res']
        Screen.__init__(self,**kwargs)
        self.ids['resgrid'].height = Window.height#bind(minimum_height=self.ids['resgrid'].setter('height'))
        self.changed = True
        #self.on_changed()
        
    def on_pre_enter(self):
        self.visible = True
        self.changed = True           
                
    def on_leave(self):  
        self.visible = False                    
        
    def on_changed(self, *args):
        if self.changed:
            self.changed = False 
            if self.visible:
                grid = self.ids['resgrid']
                grid.clear_widgets()
                grid.add_widget(Label(text='Resource'))
                grid.add_widget(Label(text='Stored'))
                grid.add_widget(Label(text='Current Price'))
                grid.add_widget(Label(text='Total Value'))
                for r in self.res.res:
                    #TODO sort resources by value or amount 
                    thisres = self.res.res[r]
                    grid.add_widget(Label(text=str(thisres.name)))
                    grid.add_widget(Label(text=str(round(thisres.amount))))
                    price = thisres.price*(resources[thisres.name]['baseval'] if thisres.name in resources else 10)
                    grid.add_widget(Label(text=str(round(price))))
                    grid.add_widget(Label(text=str(round(thisres.amount*price))))
                   

class ResourceModel(object):
    def __init__(self):
        self.res = dict()
        
        self.listpanel = ResourceScreen(res=self)
        
    def __getstate__(self):
        odict = self.__dict__.copy() # copy the dict since we change it
        del odict['listpanel']              # remove gui entry
        return odict
    
    def __setstate__(self,state):
        self.__dict__.update(state)   # update attributes
        self.listpanel = ResourceScreen(res=self)     
        
    def get_screen(self):
        return self.listpanel
        
    def changed(self):
        self.listpanel.changed = True    
        
    def check(self,res_name):
        if res_name not in self.res: self.res[res_name] = Resource(res_name)            
        
    def add(self, res_name, res_amt):
        self.check(res_name)
        self.res[res_name].add(res_amt)
        self.changed()        
    
    def sub(self, res_name, res_amt):
        self.check(res_name)
        return self.res[res_name].sub(res_amt) 
        self.changed()  
        
    def has(self, res_name, res_amt):
        self.check(res_name)
        return self.res[res_name].has(res_amt) 
        
    def amount(self, res_name):
        self.check(res_name)
        return self.res[res_name].amount
        
    def tot_amt(self):
        out=0
        for res_name in self.res:
            out += self.res[res_name].amount
        return out
     
    def price(self,res_name):
        self.check(res_name)
        val = resources[res_name]['baseval'] if res_name in resources else 10
        return self.res[res_name].price * val
         
     
    def merge(self,res):
        for r in res.res:
            self.amount(r)
            self.res[r].merge(res.res[r])
        self.changed() 
        return res            
            
        
    def split(self,amt):
        tot = self.tot_amt()
        print tot, amt
        newres = ResourceModel()
        if tot > 0: 
            frac = amt/tot 
        else:
            frac = 0
        if frac > 1: frac = 1
        for res_name in self.res:
            newres.add(res_name,self.res[res_name].amount*frac)
            newres.res[res_name].supply = self.res[res_name].supply
            newres.res[res_name].demand = self.res[res_name].demand
            newres.res[res_name].price = self.res[res_name].price
            self.sub(res_name,self.res[res_name].amount*frac)            
        self.changed()     
        return newres        
        
    #"Shopping list" funcs, taking in whole lists of resources
    def price_list(self,res_list):
        tot_val = 0
        for r in res_list:
            price = self.price(r)
            tot_val += price*res_list[r]
        return tot_val    
        
    def has_list(self,res_list): #returns a dict of booleans for each resources's fillability
        val = {}
        for r in res_list:
            val[r] = self.has(r,res_list[r])
        return val


class Resource(object):
    def __init__(self,name):
        globalvars.map.register(self)
        self.name = name
        self.amount = 0
        self.supply = 1.
        self.demand = 1.
        self.price = 1.
        self.tc = util.seconds(0.5,'day')
       
    def merge(self,res):
        if res.name != self.name: return False
        self.amount += res.amount
        res.amount = 0
        return True
        
    def add(self,amt):
        self.amount += amt
        self.supply += amt
        
    def sub(self,amt):
        self.demand += amt                
        out = min(self.amount,amt)
        self.amount -= out
        return out
        
    def has(self,amt):
        self.demand += amt/10.
        return self.amount >= amt
        
    def update(self,dt):
        if self.demand == 0 and self.supply == 0: return
        diffsum = (self.demand - self.supply)/(self.demand + self.supply)
        frac = math.exp(-dt/self.tc)
        self.supply *= frac
        self.demand *= frac
        self.price *= 1.0 + 0.1*diffsum*dt/self.tc
        
        '''self.tc *= 0.99*(3600 - dt)/3600
        
        if abs(diffsum) > 0.25: 
            self.tc *= 1.1 
            self.tc += 60'''
        #elif abs(diffsum) < 0.1:
        #    self.tc *= 0.9


class SoftResourceModel(object):
    res = dict()
    
    def check(name):              
        if 'name' not in res:
            res[name] = { 'supply':{}, 'demand:'{} }
            
    def has(name): 
        self.check(name)
        #returns 1.0 if supply >= demand, else modified efficiency     
        totsup = 1.*sum(f for f in res[name]['supply'].values())                
        totdem = 1.*sum(f for f in res[name]['demand'].values())    
        if totdem == 0
            return 1.0 if totsup > 0 else 0.0
        return min(1.0, totsup/totdem)
    
    def supply(source,name,amt):
        self.check(name)
        res[name]['supply'][source] = amt
        return self.has(name)
        
    def demand(source,name,amt):
        self.check(name)
        res[name]['demand'][source] = amt
        return self.has(name)

#    def __init__(self):


#testing            
if __name__ == "__main__":
    test = Resource('Test')
    
    for i in range(10000):
        #test.supply += random.random()
        #test.demand += 2*random.random()
        if random.random() < 0.005:
            test.supply += 100
        if random.random() < 0.5:
            test.demand += 1#random.randint(0,5)
        print test.supply, test.demand, test.price, test.tc
        test.update(60)
        
