from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.scatter import ScatterPlane
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix, Translate
from kivy.animation import Animation

import globalvars
import gps
import starfield
import numpy as np
import util

PING_SPEED = 50.

kv = '''
<MapScreen@Screen>:
    name: 'star map'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
           
    
    Starfield:
        id: stars
    MapScatterPlane:
        id: mapscale
        index: 0
        scale: 2.
        pos: self.parent.width/2,self.parent.height/2
        do_collide_after_children: True
        auto_bring_to_front: False
        do_rotation: False
        mapxy: self.parent.location[1]+self.parent.width/2,self.parent.location[0]+self.parent.height/2
        
      
                                                                                 
            
    FloatLayout:
        id: mapoverlay  
        index: 5 
        Button: 
            pos_hint: {'top': 1.00, 'right': 1.00}
            size_hint: 0.15,0.15
            text: 'Build'
            
    StackLayout:  
        id: debugoverlay  
        orientation: 'tb-lr' 
        Label:
            pos_hint: {'top': 1.00, 'left': 0.1}
            size_hint: 0.2,0.05
            text: '%02.02e %02.02e' % (self.parent.parent.location[0], self.parent.parent.location[1])
            id: loclabel 
        Label:
            pos_hint: {'top': 0.95, 'left': 0.1}
            size_hint: 0.2,0.05
            text: 'GPS off'
            id: gpslabel              
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
        
        min_side = min(Window.width, Window.height)
        globalvars.config['MAP SCALING'] = 3#(min_side - 200)/200.
        self.ids['mapscale'].scale = globalvars.config['MAP SCALING']
        print 'Resolution information:',Window.width, Window.height, globalvars.config['MAP SCALING']
        
        #Clock.schedule_interval(self.update, 0.1)               
                
    def on_leave(self):  
        self.displayed = False              
        gps.stop()
        
    def update(self,dt):
        #self.location = gps.get_location()
        self.ids['gpslabel'].text = 'ON' if gps.use_gps else 'OFF'
        return self.displayed
        
    def on_location(self, *args):
        dx = self.location[0] - self.curr_loc[0] 
        dy = self.location[1] - self.curr_loc[1]
        
        self.curr_loc = self.location
        self.ids['stars'].shift(dx,dy)
        #print self.ids['stars'].scale
        self.ids['stars'].scale = 0.001*globalvars.config['MAP SCALING']*self.ids['mapscale'].scale
        
        #print 'map',self.ids['mapscale'].mapxy
        self.ids['mapscale'].mapxy = [self.width/2 - self.location[0]*self.ids['mapscale'].scale,self.height/2 - self.location[1]*self.ids['mapscale'].scale]
        self.ids['mapscale'].update_mapxy()
        #self.ids['mapscale'].x = -globalvars.config['MAP SCALING']*self.location[0] + self.width/2 #dx*2#globalvars.config['MAP SCALING']
        #self.ids['mapscale'].y = -globalvars.config['MAP SCALING']*self.location[1] + self.height/2#dy*2#globalvars.config['MAP SCALING']
        
        anim = Animation( pos = [-globalvars.config['MAP SCALING']*self.location[0] + self.width/2,-globalvars.config['MAP SCALING']*self.location[1] + self.height/2], duration=0.5, t = 'in_out_quad' )
        anim.start(self.ids['mapscale'])
        #print self.ids['mapscale'].x, self.ids['mapscale'].y
        
    def spawn_ping(self,**kwargs):
        self.ids['mapscale'].ping(**kwargs)  
        
    def event_ping(self, extent=100, color_scheme={}):        
        loc = self.ship_loc()
        self.spawn_ping(location=loc,extent=extent,delay=0.,color=color_scheme['MAIN'] if 'MAIN' in color_scheme else [1,1,1,1])
        events = self.map.event_mgr.fetch_all(loc,extent)
        for e in events:
            self.spawn_ping(location=e.location,extent=50., delay = float(util.vec_dist(loc,e.location)/PING_SPEED),color=color_scheme[e.category] if e.category in color_scheme else [1.,1.,1.,1.],speed_factor=1.5)
        
    def ship_loc(self):
        return np.array([self.location[0],self.location[1]])        
        
    #    print args
    #    print 'loc changed!'        
                
class MapScatterPlane(ScatterPlane):
    mapxy = ListProperty([0,0])
    
    def __init__(self,**kwargs):
        super(MapScatterPlane,self).__init__(**kwargs)                
        self.trans = None
        self.update_mapxy()
        
     
        
    def update_mapxy(self,*args):   
        pass#self.pos = self.mapxy
        '''if self.trans:
            self.trans.xy = self.mapxy[0],self.mapxy[1]
        else:     
            with self.canvas.before:
                PushMatrix()                                             
                self.trans = Translate(self.mapxy[0],self.mapxy[1])                                 
            with self.canvas.after:
                PopMatrix()  ''' 

    
    def ping(self,location=None,extent=10,duration=None,delay=0.,color=[1.,1.,1.,1.],speed_factor=1.0):
        if not duration: duration = extent/(PING_SPEED*speed_factor)
        img = PingImage(source = 'img/ping/ping.png', pos=location.tolist(),color=color,size=[1,1],opacity = 0., allow_stretch=True)
        #print location, duration, delay, img
        self.add_widget(img)
        anim = Animation(opacity=0.,duration=delay) + Animation(opacity=1.,duration=0.01) + Animation(size=[extent*2.,extent*2.], center=img.center, opacity=0., duration=duration) + Animation(opacity=0.,duration=0.5)
        #anim = Animation(size=[extent*2.,extent*2.], center=img.center,duration=duration)  
        anim.bind(on_complete = img.remove_self) 
        anim.start(img)

        
class PingImage(Image):
    def remove_self(self, *args):
        if self.parent: self.parent.remove_widget(self)
        
    



