import util
import math
import numpy as np
import random

resources = {
                'Metallics': {'name':'Metallics', 'restype':'Basic', 'baseval':10},
                'Hydrates': {'name':'Hydrates', 'restype':'Basic', 'baseval':10},
                'Silicates': {'name':'Silicates', 'restype':'Basic', 'baseval':10},
                
                'DeplPhleb': {'name':'Depleted Phlebotinum', 'restype':'Basic', 'baseval':10e6},
                'ChrgPhleb': {'name':'Charged Phlebotinum', 'restype':'Basic', 'baseval':20e6},
            }

class ResourceModel(object):
    def __init__(self):
        self.res = dict()
        
    def add(self, res_name, res_amt):
        if res_name not in self.res: self.res[res_name] = Resource(res_name)
        self.res[res_name].add(res_amt)
    
    def sub(self, res_name, res_amt):
        if res_name not in self.res: self.res[res_name] = Resource(res_name)
        return self.res[res_name].sub(res_amt)  
        
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
        return self.amout >= amt
        
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
        
