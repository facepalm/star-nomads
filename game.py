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
        self.generate_map()
        #place ship in universe
        #spawn a couple of immediate events
            #one long-term, nearby
            #one short-term, nearby
            #one short-term, farther off
            
        
    def generate_map(self):            
        
        pass
        '''self.maptype = random.choice(['FOREST','GRASSLAND','VALLEY'])

        if self.maptype == 'FOREST':
            self.game_map = maps.Map(size=[300,300])
            self.game_map.vegetation.randomize('pareto',4)
            self.game_map.elevation.randomize('pareto',5)
            self.game_map.elevation.diffuse(10)
        elif self.maptype == 'GRASSLAND':
            self.game_map = maps.Map(size=[300,300])
            self.game_map.vegetation.randomize('pareto',5)
            self.game_map.elevation.randomize('pareto',5)
            self.game_map.elevation.diffuse(10)
        else: #VALLEY
            self.game_map = maps.Map(size=[500,200])
            self.game_map.vegetation.randomize('pareto',2)
            self.game_map.elevation.randomize('pareto',5)
            for i in range(0,15):
                p1 = [random.randint(0,199),random.randint(20,480)]
                p2 = [random.randint(0,199),random.randint(20,480)]
                p1[0] *= pow(p1[1]/500.,3)
                p2[0] = 199 - p2[0]*pow(p2[1]/500.,3)
                print p1, p2
                self.game_map.elevation.data[p1[1],p1[0]] = random.randint(10000,20000)*p1[1]/500.
                self.game_map.elevation.data[p2[1],p2[0]] = random.randint(10000,20000)*p2[1]/500.     
            for i in range(50): self.game_map.elevation.diffuse(5)
            self.game_map.elevation.data *= 100/self.game_map.elevation.data.max()
            
        treeline = 20    
        self.game_map.vegetation.bloom(treeline-self.game_map.elevation.data)   
            
        self.mapscreen = mapgui.MapScreen(name='Home Map')
        globalvars.root.screen_manager.add_widget(self.mapscreen) 
        self.mapscreen.ids['mapimg'].process_map(self.game_map)
            
        for i in range(0,12):            
            g = goblin.Goblin(self.game_map)
            if i==0: g.wealth=100
            self.mapscreen.ids['mapimg'].add_widget(g.image())    
            
           '''
             
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
        
