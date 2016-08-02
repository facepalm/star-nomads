import numpy as np
from scipy.stats import wald
import random
import time

import globalvars
import util
import ship
import maps

class Universe(object):    
    def __init__(self):
        self.update_time = time.time()
        
        #generate player
        #generate ship
        self.ship = ship.Premise()
        #generate universe
        self.map = maps.Map()
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
        
