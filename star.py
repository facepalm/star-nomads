import numpy as np

import logging
import random
import math

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix

import planetimages

import globalvars
import util

def initialize_star(location,density,seed,widget,_map):
    random.seed(seed)
    np.random.seed(seed if seed < 4000000000 else seed//1000000)
    if random.random() < 0.1: return None #chance there's no star here
    primary_star_mass = np.random.triangular(0.25,0.8,1.6)#wald(mean=1.5, scale=1.0, size=1)
    randomness = 0.25
    dl = np.array([random.gauss(0,randomness),random.gauss(0,randomness)])
    loc = dl*density + np.array(location)
    #print loc
    star = Star(primary_star_mass,location=loc,seed=seed)
    img = star.primary_image()
    widget.add_widget(img)    
    #widget.add_widget(Image(size_hint=(None, None),size=(1,1),pos=loc.tolist(),color=[1,0,0,1]))
    
    num_plan = random.randrange(4)
    masses = 1E24*10**(np.random.random( size=max(num_plan,1))*8 - 3)
    for p in range(num_plan):
        newp = Planet(mass=masses[p],sun=star,orbit = random.random()*star.ice_line+star.burn_line)
        star.orbiting_bodies.append(newp)
        widget.add_widget(newp.orbit_image)
    return star
    

class Star(object):
    def __init__(self, solar_masses, location, name=None, logger=None, seed=None):
        self.loc = location
        self.seed = seed
        self.is_sun = True
        globalvars.map.register(self)
        self.primary = None
        self.solar_masses = solar_masses
        self.mass = self.solar_masses*2E30
        self.name = name if name else 'Star'#util.star_name(self)
        if logger:
            self.logger = logging.getLogger(logger.name + '.' + self.name)
        else: 
            self.logger = logging.getLogger(util.generic_logger.name + '.' + self.name)
    
        #current assumption: main sequence star.  May want to simulate lifetimes and do giants in the future
        # reference: https://en.wikipedia.org/wiki/Stellar_classification
        saturation = 200.0
        if self.solar_masses < 0.5: 
            self.type = 'M'
            self.radius = 0.7
            self.luminosity = 0.08
            self.color_name = 'Red'
            self.color = np.array([255,204,111,255])/saturation
        elif self.solar_masses < 0.8: 
            frac = (self.solar_masses - 0.5)/0.3
            self.type = 'K'
            self.radius = 0.7 + 0.26*frac
            self.luminosity = 0.08 + 0.52*frac
            self.color_name = 'Orange'
            self.color = np.array([255,210,161,255])/saturation
        elif self.solar_masses < 1.04: 
            frac = (self.solar_masses - 0.8)/0.24
            self.type = 'G'
            self.radius = 0.96 + (1.15-0.96)*frac
            self.luminosity = 0.6 + (1.5 - 0.6)*frac
            self.color_name = 'Yellow'
            self.color = np.array([255, 244, 234,255])/saturation
        elif self.solar_masses < 1.4: 
            frac = (self.solar_masses - 1.04)/0.36
            self.type = 'F'
            self.radius = 1.15 + (1.4-1.15)*frac
            self.luminosity = 1.5 + (5 - 1.5)*frac
            self.color_name = 'Yellow-White'
            self.color = np.array([248, 247, 255,255])/saturation
        elif self.solar_masses < 2.1: 
            frac = (self.solar_masses - 1.4)/0.7
            self.type = 'A'
            self.radius = 1.4 + (1.8-1.4)*frac
            self.luminosity = 5 + (25 - 5)*frac
            self.color_name = 'White'
            self.color = np.array([202, 215, 255,255])/saturation   
        elif self.solar_masses < 16: 
            frac = (self.solar_masses - 2.1)/(16-2.1)
            self.type = 'B'
            self.radius = 1.8 + (6.6-1.8)*frac
            self.luminosity = 25 + (30000 - 25)*frac
            self.color_name = 'Blue-White'  
            self.color = np.array([170, 191, 255,255])/saturation 
        else: # self.solar_masses > 16: 
            frac = (self.solar_masses - 2.1)/(16-2.1)
            self.type = 'O'
            self.radius = 8 #arbitrary
            self.luminosity = 50000 #arbitrary
            self.color_name = 'Blue'     
            self.color = np.array([155, 176, 255,255])/saturation 
        
        #tone down luminosity, which leads to crazy (but accurate!) distances with bright stars        
        self.luminosity = pow( self.luminosity , 0.75)
        
        self.habitable_start = 0.80 * pow( self.luminosity ,0.5) #0.8
        self.habitable_end = 5 * pow( self.luminosity ,0.5)   #1.4
        
        self.burn_line = 0.5 * pow( self.luminosity ,0.5)
        self.snow_line = 10 * pow( self.luminosity ,0.5) #3
        self.ice_line = 20 * pow( self.luminosity ,0.5) #10
        self.system_line = 30 * pow( self.luminosity ,0.5) #40, arbitrary
        
        self.explored = 0.0
        self.orbiting_bodies = []
        
        #self.view = systempanel.SystemScreen(name=util.short_id(self.id)+"-system",primary=self)
        

    def primary_image(self):
        frac = 0.3        
        img = Image(source='img/sun/generic_sun.png',color=self.color,mipmap=True,center=self.loc.tolist(),allow_stretch=False,size_hint=(None, None),size=(round(75*frac*self.radius), round(75*frac*self.radius)))
        img.center=self.loc.tolist()
        return img
        
    def random_habitable_orbit(self):
        return (random.random()*0.6 + 0.8) * pow( self.luminosity ,0.5)
        
    def is_habitable(self,orbit):
        return self.habitable_start < orbit and orbit < self.habitable_end
    
    def info(self):
        out = self.type+'-type star, with mass of %.2f' % self.solar_masses + ' and luminosity of %.2f' % self.luminosity
        out += ', Habitable zone between %.2f' % self.habitable_start +' and %.2f' % self.habitable_end
        out += ', Snow line at %.2f' % self.snow_line
        return out
        
    def add_exploration(self,amt=0.0001,limit=0.1):
        if self.explored < limit: self.explored += amt   
        
    def proximity(self,loc=None):
        if loc is None: return 'Deep space'
        dist = self.loc_to_orbit(loc)
        if dist < self.burn_line: return 'Near star'
        if self.is_habitable(dist): return 'Goldilocks'
        if dist < self.snow_line: return 'Inner system'
        if dist < self.ice_line: return 'Outer system'
        if dist < self.system_line: return 'Kuiper belt'
        return 'Deep space'
        
    def random_location(self,rough_orbit=3):
        orbit = rough_orbit*(0.9+0.2*random.random())        
        pos = 2 * math.pi * random.random()
        return [float(self.loc[0] + math.cos(pos)*orbit), \
                float(self.loc[1] + math.sin(pos)*orbit)]
                
    def loc_to_orbit(self,loc):        
        return util.vec_dist(self.loc, np.array(loc))/globalvars.M_TO_AU
        
        
class Planet(object):
    def __init__(self,mass=None,sun=None,orbit=None,name=None, logger=None):
        globalvars.map.register(self)
        self.is_sun = False
        self.mass = mass if mass else 1E21*random.paretovariate(2)
        self.name = name if name else 'Planet'#util.planet_name(self)
        self.primary=sun
        self.orbit = orbit        
        
        #estimate radius, based off Earth
        self.radius = 6400000 *pow(self.mass/6E24,0.3)
                
        #calculate orbital period
        #T = 2pi*sqrt(a^3/u)
        mu = 6.674E-11 * self.primary.mass
        mmu = 6.674E-11 * self.mass
        a = self.orbit * 149597870700.
        self.orbital_period = 2 * math.pi * pow(pow(a,3)/mu,0.5)
        
        #self.launch_dv = pow( mmu/ (self.radius + 500000) , 0.5 )
        
        if logger:
            self.logger = logging.getLogger(logger.name + '.' + self.name)
        else: 
            self.logger = logging.getLogger(util.generic_logger.name + '.' + self.name)
    
        self.color = None #assign color to enable tinting
        self.img_name = 'generic_sun.png'        
        self.img_radius = 0.25
        
        if self.mass > 1E29: 
            self.type = 'INVALID' #actually a sun.  Throw an error, this shouldnt happen
        elif self.mass > 1E28: 
            self.type = 'Brown dwarf' #counting this as a planet, since they have negligible radiation    
            self.img_radius = 0.5
        elif self.mass > 1E26:
            self.type = 'Gas giant'
            self.img_radius = 0.5
            '''if self.orbit < self.sun.ice_line:
                self.type = 'Gas giant' 
                saturation = 255.0
                self.color = random.choice([np.array([255, 141, 110,255])/saturation, np.array([255, 198, 110,255])/saturation])
                #self.radius = 
            else:
                saturation = 255.0
                self.type = 'Ice giant'
                self.color = random.choice([np.array([228, 250, 250,255])/saturation, np.array([11, 41, 255, 255])/saturation])
            self.img_name = 'generic_sun.png'''
            
        elif self.mass > 1E23:
            self.type = 'Planet' #rocky world, but capable of retaining an atmosphere, even if barely
        elif self.mass > 1E21:
            self.type = 'Dwarf planet' #larger moons and asteroids, rounded
            self.img_radius = 0.2
        else:
            self.type = 'Planetoid' #small moons, asteroids, rocks, etc
            self.img_name = 'generic_asteroid.png'
            self.img_radius = 0.10
    
    
        self.explored = 0.0
        #self.resources = planetresources.PlanetResources(self)
        self.occupied = 0
        #self.initialize_sites()
        
        self.orbiting_bodies = []
        
        self.orbit_pos = random.random()*2*3.14159
        
        
        self.image = planetimages.random_image(self)
        

        #self.generate_primary_image()        
        self.generate_orbital_image()                        
        
        #self.view = systempanel.SystemView(primary=self)
        #self.view = systempanel.SystemScreen(name=util.short_id(self.id)+"-system",primary=self)
        
    def escape_velocity(self):
        mmu = 6.674E-11 * self.mass                
        v = pow( 2*mmu/ (self.radius + 500000.0) , 0.5 ) - self.launch_dv()
        return v

    def launch_dv(self):
        mmu = 6.674E-11 * self.mass
        return pow( mmu/ (self.radius + 500000) , 0.5 )
                
        
    '''def initialize_sites(self):
        self.sites=[]
        self.num_sites = 6 if self.type == 'Planet' else 2 if self.type == 'Dwarf planet' else 1 if self.type == 'Planetoid' else 0
        self.num_orbits = 1
        for s in range(self.num_orbits):
            s1 = planetsite.PlanetSite(self,'Orbit'+str(s))
            self.sites.append(s1)

        for s in range(self.num_sites):
            s1 = planetsite.PlanetSite(self,'Site'+str(s))
            self.sites.append(s1)'''
        
    def primary_image(self):
        return planetimages.load_primary(self, self.image)

        if self.color is not None: 
            self.image.color=self.color
   
    def mugshot_image(self):                
        return planetimages.load_panel(self, self.image)
        
    
    def generate_orbital_image(self):         
        self.orbit_image = planetimages.load_orbital(self, self.image,radius=self.img_radius)


        
    '''def update(self,dt):

        secs = dt*globalvars.config['TIME FACTOR']
        old_pos = self.orbit_pos        
        self.orbit_pos += (secs/self.orbital_period)*2*3.14159
        if self.orbit_pos > 2*math.pi: self.orbit_pos -= 2*math.pi
        #print self.orbit_pos - old_pos
        self.orbit_image.orbit_pos = self.orbit_pos
        
        self.occupied=0
        for o in self.orbiting_bodies:
            self.occupied = max(self.occupied,o.occupied)
        for s in self.sites:
            s.update_occupied()
            self.occupied = max(self.occupied,s.occupied)'''

    def add_exploration(self,amt=0.0001,limit=0.1):
        if self.explored < limit: self.explored += amt        
        
