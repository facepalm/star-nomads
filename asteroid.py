import random

import util
import resources

class Asteroid(object):
    def __init__(self,location=None,star=None,mass = None, differentiation = 0.):

        self.star=star
        #if self.star is None: 
        differentiation = max(0.,min(1.,differentiation))
            
        self.loc = location if location is not None else self.star.random_location() if self.star is not None else [0,0]
        
        #get point in space (inner, outer, kuiper, oort, deep) and location (orbit, belt, deep)
        self.position = self.star.proximity(self.loc) if self.star is not None else 'Deep space'
                
        #generate properties
        self.basic_types = ['Metallics','Silicates','Hydrates']
        random.shuffle(self.basic_types)
        
        mass = mass if mass else 1E6
        
        self.composition = resources.ResourceModel()
        for i in self.basic_types:
            self.composition.add(i, mass*differentiation)
            mass *= 1-differentiation
        
        for i in self.basic_types:
            self.composition.add(i, mass*differentiation/3.)
        
        if self.position in ['Near star','Goldilocks','Inner system']:
            self.composition.sub('Hydrates',0.9*self.composition.amount('Hydrates'))
        
        
