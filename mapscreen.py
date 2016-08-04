from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty

import globalvars
import gps
import starfield

kv = '''
<MapScreen@Screen>:
    name: 'star map'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
    
    Starfield:
        id: stars
    Scatter:
        id: mapscale
        index: 0
        pos: self.parent.width/2,self.parent.height/2
        do_collide_after_children: True
        auto_bring_to_front: False
        do_rotation: False
        
        Label:
            pos_hint: {'center_x': 0., 'center_y': 1.0}
            text: '%f %f' % (self.parent.parent.location[0], self.parent.parent.location[1])
    FloatLayout:
        id: mapoverlay  
        index: 5 
        Button: 
            pos_hint: {'top': 1.00, 'right': 1.00}
            size_hint: 0.15,0.15
            text: 'Build'
'''

Builder.load_string(kv)

class MapScreen(Screen):
    location = ListProperty([0, 0])

    def __init__(self,**kwargs):
        super(MapScreen,self).__init__(**kwargs)
        self.map = kwargs['map'] if 'map' in kwargs else None
        self.displayed = False
        self.curr_loc = [0,0]
        
    def on_pre_enter(self):
        gps.start()
        self.displayed = True
        if self.map is not None:
            if self.map.ship is not None:
                pass
        Clock.schedule_interval(self.update, 0.1)               
                
    def on_leave(self):  
        self.displayed = False              
        gps.stop()
        
    def update(self,dt):
        self.location = gps.get_location()
        
        return self.displayed
        
    def on_location(self, *args):
        dx = self.location[0] - self.curr_loc[0] 
        dy = self.location[1] - self.curr_loc[1]
        
        self.curr_loc = self.location
        self.ids['stars'].shift(dx,dy)
    #    print args
    #    print 'loc changed!'        
                
        
    
    



