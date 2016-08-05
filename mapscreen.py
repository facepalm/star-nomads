from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix, Translate

import globalvars
import gps
import starfield

kv = '''
<MapScreen@Screen>:
    name: 'star map'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
    
    Starfield:
        id: stars
    ScatterPlane:
        id: mapscale
        index: 0
        pos: 0,0 #self.parent.width/2,self.parent.height/2
        do_collide_after_children: True
        auto_bring_to_front: False
        do_rotation: False
        
        canvas:
            Line:
                points: [0, 0, 10, 10, 10, 0]
            Translate: 
                xy: self.parent.location[1]+self.parent.width/2,self.parent.location[0]+self.parent.height/2
             
            
                                
        
        Label:
            center: 0,0 #_hint: {'center_x': 0., 'center_y': 1.0}
            text: '%f %f' % (self.parent.parent.location[0], self.parent.parent.location[1])
        Label:
            center: 0,-30
            text: 'GPS off'
            id: gpslabel
        
            
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
        self.ids['gpslabel'].text = 'ON' if gps.use_gps else 'OFF'
        return self.displayed
        
    def on_location(self, *args):
        dy = self.location[0] - self.curr_loc[0] 
        dx = self.location[1] - self.curr_loc[1]
        
        self.curr_loc = self.location
        self.ids['stars'].shift(dx,dy)
        
    #    print args
    #    print 'loc changed!'        
                
class MapScatter(Scatter):
    pass
    '''def __init__(self,**kwargs):
        super(MapScatter,self).__init__(**kwargs)                
        
        with self.canvas.before:
            PushMatrix()                                             
            Translate(self.parent.location[1],self.parent.location[0]) 
            
            
        with self.canvas.after:
            PopMatrix()   '''
        
    
    



