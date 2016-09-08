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


resources = {
                'Slag': {'name':'Slag', 'restype':'Basic', 'baseval':5}, #crap tier, rejects from other process that need processing just to be raw again
                'Waste': {'name':'Waste', 'restype':'Basic', 'baseval':5},    
        
                'Metallics': {'name':'Metallics', 'restype':'Basic', 'baseval':10}, #raw resource tier
                'Hydrates': {'name':'Hydrates', 'restype':'Basic', 'baseval':10},
                'Silicates': {'name':'Silicates', 'restype':'Basic', 'baseval':10},
                'Organics': {'name':'Organics', 'restype':'Basic', 'baseval':10},                
                
                'Metals': {'name':'Metals', 'restype':'Basic', 'baseval':20},
                'Water': {'name':'Water', 'restype':'Basic', 'baseval':20},
                'Carbon': {'name':'Carbon', 'restype':'Basic', 'baseval':20},
                'Silicon': {'name':'Silicon', 'restype':'Basic', 'baseval':20},
                
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
    def __init__(self,**kwargs):
        self.res = kwargs['res']
        Screen.__init__(self,**kwargs)
        self.ids['resgrid'].height = Window.height#bind(minimum_height=self.ids['resgrid'].setter('height'))
        self.changed = True
        #self.on_changed()
        
    def on_changed(self, *args):
        if self.changed:
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
            self.changed = False        

class ResourceModel(object):
    def __init__(self):
        self.res = dict()
        
        self.listpanel = ResourceScreen(res=self)
        
    def get_screen(self):
        return self.listpanel
        
    def changed(self):
        self.listpanel.changed = True        
        
    def add(self, res_name, res_amt):
        if res_name not in self.res: self.res[res_name] = Resource(res_name)
        self.res[res_name].add(res_amt)
        self.changed()        
    
    def sub(self, res_name, res_amt):
        if res_name not in self.res: self.res[res_name] = Resource(res_name)
        return self.res[res_name].sub(res_amt) 
        self.changed()  
        
    def has(self, res_name, res_amt):
        if res_name not in self.res: self.res[res_name] = Resource(res_name)
        return self.res[res_name].has(res_amt) 
        
    def amount(self, res_name):
        if res_name not in self.res: self.res[res_name] = Resource(res_name)
        return self.res[res_name].amount
        
    def tot_amt(self):
        out=0
        for res_name in self.res:
            out += self.res[res_name].amount
        return out
     
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


class Resource(object):
    def __init__(self,name):
        self.id = util.register(self)
        self.name = name
        self.amount = 0
        self.supply = 1.
        self.demand = 1.
        self.price = 1.
        self.tc = 3600. 
       
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
        return self.amount >= amt
        
    def update(self,dt):
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
        
