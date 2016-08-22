import numpy as np

import logging
import random
import math

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix

import globalvars
import util

def initialize_star(location,density,seed):
    random.seed(seed)
    np.random.seed(seed)
    if random.random() < 0.1: return None #chance there's no star here
    primary_star_mass = np.random.wald(mean=1.0, scale=1.5, size=1)
    randomness = 0.5
    dl = np.array([random.gauss(0,randomness),random.gauss(0,randomness)])
    loc = dl*density + np.array(location)*density
    star = Star(primary_star_mass,loc,seed=seed)
    return star
    

class Star(object):
    def __init__(self, solar_masses, location, name=None, logger=None, seed=None):
        self.loc = location
        self.seed = seed
        self.is_sun = True
        self.id = util.register(self)
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
        
        self.habitable_start = 0.80 * pow( self.luminosity ,0.5)
        self.habitable_end = 1.4 * pow( self.luminosity ,0.5)
        
        self.snow_line = 3 * pow( self.luminosity ,0.5)
        self.ice_line = 10 * pow( self.luminosity ,0.5)
        
        self.explored = 0.0
        self.orbiting_bodies = []
        
        #self.view = systempanel.SystemScreen(name=util.short_id(self.id)+"-system",primary=self)
        

    def primary_image(self):
        frac = 0.5        
        return Image(source='img/sun/generic_sun.png',color=self.color,mipmap=True,center=self.loc.tolist(),allow_stretch=True,size_hint=(None, None),size=(round(75*frac*self.radius), round(75*frac*self.radius)))
        
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
