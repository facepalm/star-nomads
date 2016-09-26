import random
import copy
from kivy.uix.image import Image
from kivy.uix.bubble import Bubble
from kivy.lang import Builder


import util
import resources
import globalvars

class Asteroid(object):
    def __init__(self,location=None,star=None,mass = None, differentiation = None):
        globalvars.map.register(self)
        self.identity = 'asteroid'
        
        self.star=star
        #if self.star is None: 
        if differentiation is None: differentiation = random.random()*1.0#0.1
        differentiation = max(0.,min(1.,differentiation))
        self.differentiation = differentiation
            
        self.loc = location if location is not None else self.star.random_location() if self.star is not None else [0,0]
        
        #get point in space (inner, outer, kuiper, oort, deep) and location (orbit, belt, deep)
        self.position = self.star.proximity(self.loc) if self.star is not None else 'Deep space'
                
        #generate properties
        self.basic_types = ['Metallics','Silicates','Hydrates','Organics']
        random.shuffle(self.basic_types)
        
        mass = mass if mass else 1E7
        self.image = None
        
        self.composition = resources.ResourceModel()
        for i in self.basic_types:
            self.composition.add(i, mass*differentiation)
            mass *= 1-differentiation
        
        for i in self.basic_types:
            self.composition.add(i, mass/len(self.basic_types))
        
        if self.position in ['Near star','Goldilocks','Inner system']:
            self.composition.sub('Hydrates',0.9*self.composition.amount('Hydrates'))
            
        print 'Asteroid mass:', self.mass()
            
    def mass(self):
        return self.composition.tot_amt()            
        
    def split(self,amt):
        if amt <= 0: return None
        newres = self.composition.split(amt)
        
        newast = copy.copy(self)
        globalvars.map.register(newast)
        newast.composition = newres
        newast.get_image(reset=True)
        
        if self.image and self.image.parent:
            self.image.parent.add_widget(newast.image)
        if self.composition.tot_amt() <= 0:
            #used up all of us.  Die
            self.leave_map()
        return newast        
        
    def leave_map(self):              
        self.image.suicide()
        
    def coloration(self):
        if self.basic_types[0] == 'Hydrates': return [0.75, 0.75, 0.95, 1.0]        
        if self.basic_types[0] == 'Metallics': return [0.84, 0.36, 0.16, 1.0]    #'d85c2aff'
        if self.basic_types[0] == 'Organics' or self.differentiation < 0.25: return [0.4, 0.4, 0.4, 1.0]
        return [0.8, 0.8, 0.8, 1.0]
        
    def get_image(self,reset=False):
        frac = 0.3      
        if not reset and self.image is not None: return self.image  
        img = AsteroidImage(source='img/generic_asteroid.png',color=self.coloration(),mipmap=True,center=self.loc.tolist(),allow_stretch=False,size_hint=(None, None),size=(10,10),asteroid=self)
        img.center=self.loc.tolist()
        self.image = img
        return img        
        
    def touched(self,touch):
        '''The player touched this asteroid, spawn some kind of dialog'''
        #print 'Asteroid harvested?', touch
        
        bubble = AsteroidBubble(asteroid=self)
        bubble.pos = touch
          
        self.image.parent.mapscreen.ids['mapoverlay'].add_widget(bubble)       
        
    def suicide(self):
        globalvars.map.unregister(self) #will no longer update        
        self.image.suicide()        
        
    def txt_info(self):
        out = ''
        out += 'Asteroid '+util.short_id(self.id)+'\n'
        out += 'Stony' if self.basic_types[0] == 'Silicates' else 'Metal' if self.basic_types[0] == 'Metallics' else 'Chondrite' if self.basic_types[0] == 'Organics' else 'Icy'
        out += ' ({0:1.2f}%)\n'.format(100.*self.composition.amount(self.basic_types[0])/self.mass()) 
        out += 'Estimated yield: ' + "{0:0.1e}".format(self.mass()) + ' kg'
        return out
        
                
    def __getstate__(self):
        odict = self.__dict__.copy() # copy the dict since we change it
        del odict['image']              # remove gui entry
        return odict
    
    def __setstate__(self,state):
        self.__dict__.update(state)   # update attributes
        self.image = None
        self.get_image()

kv='''
<AsteroidBubble>:
    orientation: 'vertical'
    size_hint: (None, None)
    Label:
        id: asteroid_info
        text: "Shouldn't see this"       
    BubbleButton:
        text: 'Harvest'    
        on_press: self.parent.parent.on_harvest()
        size_hint: 1, 0.5
    
'''

Builder.load_string(kv)

class AsteroidBubble(Bubble):
    def __init__(self,**kwargs):
        Bubble.__init__(self,**kwargs)
        self.ast = kwargs['asteroid']
        self.ids['asteroid_info'].text = self.ast.txt_info()
        self.ids['asteroid_info'].texture_update()        
        #resize?
        
        self.size = self.ids['asteroid_info'].texture_size
        print self.size
        self.width += 10
        self.height += 40
        
    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)       
        touch.pop()
        if not touched:
            self.parent.remove_widget(self)
        return super(AsteroidBubble, self).on_touch_down(touch)   
        
    def on_harvest(self,*args):
        harv = globalvars.universe.ship.harvest(self.ast)
        globalvars.universe.status_log.add(harv[1])
        if harv[0]: self.parent.remove_widget(self)
        
        
class AsteroidImage(Image):
    def __init__(self,**kwargs):
        self.asteroid = kwargs['asteroid']        
        Image.__init__(self,**kwargs)

    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)
        touch.apply_transform_2d(self.to_window)
        tpos = touch.pos        
        touch.pop()
        if touched:
            self.asteroid.touched(tpos)
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(AsteroidImage, self).on_touch_down(touch)     
        
    def suicide(self):
        if self.parent:
            self.parent.remove_widget(self)            
