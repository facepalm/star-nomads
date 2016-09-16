import numpy as np
import random
import time

import globalvars
import util
import ship
import maps
from PIL import Image

class Universe(object):    
    def __init__(self):
        self.update_time = time.time()
        
        #galactic map        
        self.galaxy_stars = np.array(Image.open('img/galaxy/m100_apod_JudySchmidt_CC3/star_density.png'))
        self.galaxy_dust = np.array(Image.open('img/galaxy/m100_apod_JudySchmidt_CC3/dust_density.png'))
        self.galaxy_display = Image.open('img/galaxy/m100_apod_JudySchmidt_CC3/m100_hubble_4060-downsampled.png')
        
        #generate player
        #generate ship
        
        #generate universe
        self.map = maps.Map(universe=self)
        self.ship = ship.Premise()
        self.map.new_player_ship(self.ship)
        globalvars.root.screen_manager.add_widget(self.map.display)
        
        #self.map.spawn('asteroid',[30,30])
        self.map.spawn('asteroid',[90,30])
        
        self.map.update(0)
        #globalvars.root.onNextScreen(self.map.display.name, transition='None')
        
        #place ship in universe
        #spawn a couple of immediate events
            #one long-term, nearby
            #one short-term, nearby
            #one short-term, farther off
            
                     
        #globalvars.root.screen_manager.current = self.mapscreen.name
            
        #imdata = self.game_map.vegetation.data.copy()
        #print imdata
        #m = max(imdata.ravel())
        #imdata = np.divide(imdata,m)
        
        #cv2.imshow('rawfield', imdata)
        #cv2.waitKey(100)   
        
        

    def update(self,dt):
        #self.mapscreen.ids['mapimg'].refresh_map()
        deet = (time.time() - self.update_time)
        self.update_time += deet
        secs = deet*globalvars.config['TIME FACTOR']
        print 'Time delay:',secs
        for obj in globalvars.ids.values():
            if hasattr(obj,'update'):
                obj.update(secs)

    def map_update(self,dt):
        self.game_map.update_layers()
                
    def add_exploration(self,amt=0.0001,limit=0.1):
        for obj in globalvars.ids.values():
            if isinstance(obj,planet.Planet) or isinstance(obj,planet.Star):
                obj.add_exploration(amt,limit)
        
