import random
from kivy.uix.image import Image

import util
import resources
import globalvars

class Asteroid(object):
    def __init__(self,location=None,star=None,mass = None, differentiation = 0.):

        self.identity = 'asteroid'
        
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
        self.image = None
        
        self.composition = resources.ResourceModel()
        for i in self.basic_types:
            self.composition.add(i, mass*differentiation)
            mass *= 1-differentiation
        
        for i in self.basic_types:
            self.composition.add(i, mass*differentiation/3.)
        
        if self.position in ['Near star','Goldilocks','Inner system']:
            self.composition.sub('Hydrates',0.9*self.composition.amount('Hydrates'))
            
    def mass(self):
        return self.composition.tot_amt()            
        
    def split(self,amt):
        if amt <= 0: return None
        newres = self.composition.split(amt)
        if self.composition.tot_amt() <= 0:
            #used up all of us.  Die
            return self
        newast = self.clone()
        newast.composition = newres
        newast.get_image(reset=True)
        self.image.parent.add_widget(newast.image)
        return newast        
        
    def leave_map(self):              
        if self.image.parent is not None: self.image.parent.remove_widget(self.image)
        
    def coloration(self):
        if self.basic_types[0] == 'Hydrates': return [0.75, 0.75, 0.95, 1.0]        
        if self.basic_types[0] == 'Metallics': return [0.84, 0.36, 0.16, 1.0]    #'d85c2aff'
        return [0.8, 0.8, 0.8, 1.0]
        
    def get_image(self,reset=False):
        frac = 0.3      
        if not reset and self.image is not None: return self.image  
        img = AsteroidImage(source='img/generic_asteroid.png',color=self.coloration(),mipmap=True,center=self.loc.tolist(),allow_stretch=False,size_hint=(None, None),size=(10,10),asteroid=self)
        img.center=self.loc.tolist()
        self.image = img
        return img        
        
    def touched(self):
        '''The player touched this asteroid, spawn some kind of dialog'''
        print 'Asteroid harvested?'   
        globalvars.universe.ship.harvest(self)
        
class AsteroidImage(Image):
    def __init__(self,**kwargs):
        self.asteroid = kwargs['asteroid']        
        Image.__init__(self,**kwargs)

    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)
        touch.pop()
        if touched:
            self.asteroid.touched()
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(AsteroidImage, self).on_touch_down(touch)        
