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
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix, Translate
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import math

import globalvars
import gps
import starfield
import numpy as np
import util
from functools import partial
import buildscreen

PING_SPEED = 50.

btn_icons = {'Dock' : 'img/icon/noun-project/icon54-port.png',
             'Build': 'img/icon/noun-project/rob-armes-mining-tools.png'}

kv = '''
<MapScreen@Screen>:
    name: 'star map'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
           
    
    Starfield:
        id: stars
    MapScatterPlane:
        id: mapscale
        mapscreen: self.parent
        index: 0
        scale: 2.
        pos: self.parent.width/2,self.parent.height/2
        do_collide_after_children: True
        auto_bring_to_front: False
        do_rotation: False
        
        #Image:
        #    size: 1,1
        #    color: 1,1,0,1
        #    center: self.parent.parent.location
        canvas.before:
            Color:
                rgba: .2, .2, .2, .5
            Ellipse: 
                pos: self.parent.location[0] - self.parent.accuracy,self.parent.location[1] - self.parent.accuracy
                size: 2*self.parent.accuracy,2*self.parent.accuracy
                    
      
                                                                                 
            
    FloatLayout:
        id: mapoverlay  
        index: 5 
        StackLayout: 
            id: status
            size_hint_x: 0.2
            size_hint_y: None
            height: self.width
            orientation: 'lr-bt'
            
            pos_hint: {'top': 1.00, 'right': 1.00}
            #Image:
            #    mipmap: True
            #    size_hint: 0.1, 0.1
            #    pos_hint: {'x': 0.0, 'left': 1.00}
            #    id: systemposition
            #    source: 'img/icon/sun.png'
            #    color: 1.0, 0.95, 0.05, 1.0
                
        BoxLayout:
            id: menus
            size_hint_x: 1.0
            size_hint_y: 0.1
            #height: self.width/4 
            #orientation: 'lr-bt'
            pos_hint: {'y': 0.00, 'right': 1.00}
            
            Button:
                size_hint: None, 1.0
                width: self.height
                pos_hint: {'x': 0.0, 'left': 1.00}
                id: shippanelbtn          
                on_press: self.parent.parent.parent.on_shippanel_button()
                BoxLayout:
                    pos: self.parent.pos
                    size: self.parent.size
                
                    Image:
                        source: 'img/icon/noun-project/mister-pixel-rocket.png'
                        color: 0.1, 1.0, 0.1, 1.0
                        size_hint: 0.9,0.9
                        pos_hint: {'center_x': 0.5, 'center_y': .5}
                        mipmap: True
                                
                        
            Button:
                size_hint: None, 1.0
                width: self.height
                pos_hint: {'x': 0.0, 'left': 1.00}
                status: 'DOCK'
                id: dockbuildbtn   
                on_press: self.parent.parent.parent.on_dockbuild_button()             
                BoxLayout:
                    pos: self.parent.pos
                    size: self.parent.size
                    
                    Image:
                        id: dockbuildimg
                        source: 'img/icon/noun-project/icon54-port.png'
                        color: 0.1, 1.0, 0.1, 1.0
                        size_hint: 0.9,0.9
                        pos_hint: {'center_x': 0.5, 'center_y': .5}
                        mipmap: True                        
                        
            Button:
                size_hint: None, 1.0
                width: self.height
                pos_hint: {'x': 0.0, 'left': 1.00}
                id: galmapbtn   
                on_press: self.parent.parent.parent.on_galmappanel_button()             
                BoxLayout:
                    pos: self.parent.pos
                    size: self.parent.size
                    
                    Image:
                        source: 'img/icon/noun-project/combine-design-galaxy.png'
                        color: 0.1, 1.0, 0.1, 1.0
                        size_hint: 0.9,0.9
                        pos_hint: {'center_x': 0.5, 'center_y': .5}
                        mipmap: True                        
                        
            Button:
                id: statusdisplay
                size_hint: 0.5, 1.0
                text_size: self.size[0]*0.9, self.size[1]*0.9
                halign: 'left'
                valign: 'middle'
                on_press: self.parent.parent.parent.on_log_button()             
                text:"Test text doo doo de doo tjlkasldkjadl\\n fhjklhdzfk jhzdslkf"                                                       
                    
                        
            
    StackLayout:  
        id: debugoverlay  
        orientation: 'tb-lr' 
        Label:
            pos_hint: {'top': 1.00, 'left': 0.2}
            size_hint: 0.5,0.05
            text: '%d %d %d' % (self.parent.parent.location[0], self.parent.parent.location[1], self.parent.parent.accuracy)
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
    accuracy = NumericProperty(50)

    def __init__(self,**kwargs):
        self.map = kwargs['map'] if 'map' in kwargs else None
        super(MapScreen,self).__init__(**kwargs)
        

        self.name = 'Star Map -'+util.short_id(self.map.id)
        
        self.Builder = None
        
        self.displayed = False
        self.curr_loc = [0,0]
        
        self.ids['stars'].density = 500./self.map.density
        self.ids['stars'].on_size()
        
        self.accum_dist = 0
        
        self.anim = None
        
        self.touched = False
        self.touch_event = None
        
    def on_shippanel_button(self):
        if self.map and self.map.ship:
        
            self.map.ship.touched()        
        
    def on_respanel_button(self):
        if self.map and self.map.ship:
            globalvars.root.switchScreen(self.map.ship.storage.get_screen())   
            
    def on_galmappanel_button(self):
        globalvars.root.switchScreen(self.map.universe.galaxy_map)

    def on_dockbuild_button(self):        
        btn = self.ids['dockbuildbtn']
        print "Attempting to dock and/or build something:", btn.status
        if btn.status == 'DOCK':
            obj = self.map.fetch_objects(self.location,self.map.ship.sensor_strength() )
            print obj
            if obj == []: return False
            if len(obj) > 1: #m
                print 'More than one dockable in range!  resolve'
        elif btn.status == 'BUILD':
            print 'Attempting to build something'
            #build window?
            globalvars.root.switchScreen(buildscreen.BuildScreen(location=self.location)) 
            
    def on_log_button(self):
        globalvars.root.switchScreen(globalvars.universe.status_log.screen)            
        
    def on_pre_enter(self):
        gps_status = gps.start()
        print "Turning GPS on, result ", gps_status
        self.displayed = True
        
        min_side = min(Window.width, Window.height)
        globalvars.config['MAP SCALING'] = (min_side - 200)/200.
        self.ids['mapscale'].scale = globalvars.config['MAP SCALING']
        print 'Resolution information:',Window.width, Window.height, globalvars.config['MAP SCALING']
        
        #Clock.schedule_interval(self.update, 0.1)               
        
        globalvars.universe.status_log.screen.status_display = self.ids['statusdisplay']
        globalvars.universe.status_log.screen.refresh()
                
        self.curr_loc = [0,0]
        self.update_location()        
                
    def on_leave(self):  
        self.displayed = False              
        gps.stop()
        
    def on_enter(self):
        #self.ids['mapscale'].scale = globalvars.config['MAP SCALING']
        self.ids['mapscale'].propagate_scale()
        self.update_location()    
        
    def update(self,dt=0):
        #self.location = gps.get_location()
        self.ids['gpslabel'].text = 'ON' if gps.gps_on else 'OFF'
        self.touched=False  
        self.accuracy = gps.accuracy
        
        #check if the dockbuild button should be dock or build
        obj = self.map.fetch_objects(self.location,10)
        print obj
        btn = self.ids['dockbuildbtn']
        if obj == [] and btn.status == 'DOCK':
            self.ids['dockbuildimg'].source = btn_icons['Build']
            btn.status = 'BUILD'
            btn.texture_update()
        elif obj != [] and btn.status == 'BUILD':
            self.ids['dockbuildimg'].source = btn_icons['Dock']
            btn.status = 'DOCK'
            btn.texture_update()
        
        return self.displayed
        
    def on_location(self,*args):    
        pass
        
    def reset_camera(self,duration=0.01):
        self.accum_dist = 0
        if duration > 0.3:
            anim = Animation( pos = [-globalvars.config['MAP SCALING']*self.location[0] + self.width/2,-globalvars.config['MAP SCALING']*self.location[1] + self.height/2], duration = duration )#, t='in_out_sine')        
            anim &= Animation( scale = globalvars.config['MAP SCALING'], duration = duration)       
            anim.start(self.ids['mapscale'])
            self.anim = anim
        else: #just do it instantly, don't bother animating
            self.ids['mapscale'].scale = globalvars.config['MAP SCALING']
            self.ids['mapscale'].pos = [-globalvars.config['MAP SCALING']*self.location[0] + self.width/2,-globalvars.config['MAP SCALING']*self.location[1] + self.height/2]
            #self.ids['mapscale'].propagate_scale()
        #Clock.schedule_once(self.ids['mapscale'].propagate_scale,duration)
        
    def update_location(self, *args):
        dx = self.location[0] - self.curr_loc[0] 
        dy = self.location[1] - self.curr_loc[1]
        
        dist = math.sqrt(dx**2 + dy**2)
        self.accum_dist += dist
        animate = False if self.curr_loc == [0,0] or dist >= 10000 else True
        print "animate", animate, self.curr_loc, dist, gps.bearing
        self.ids['stars'].animation = animate
        
        self.curr_loc = self.location
        if animate: self.ids['stars'].shift(dx,dy)
        #print self.ids['stars'].scale
        self.ids['stars'].scale = 0.001*globalvars.config['MAP SCALING']*self.ids['mapscale'].scale
        
        duration = 1.0 if animate and self.accuracy < 20 else 0.01
        if not self.touched and self.accum_dist >= 20:           
            print "resetting camera!"
            self.reset_camera(duration=duration)
            
        
    def spawn_ping(self,**kwargs):
        self.ids['mapscale'].ping(**kwargs)  
        
    def event_ping(self, extent=100, color_scheme={}):        
        loc = self.ship_loc()
        self.spawn_ping(location=loc,extent=extent,delay=0.,color=color_scheme['MAIN'] if 'MAIN' in color_scheme else [1,1,1,1])
        events = self.map.event_mgr.fetch_all(loc,extent)
        for e in events:
            dist = util.vec_dist(loc,e.location)
            self.spawn_ping(location=e.location,extent=float(50.*(dist/100.)), delay = float(util.vec_dist(loc,e.location)/PING_SPEED),duration=1.0,color=color_scheme[e.category] if e.category in color_scheme else [1.,1.,1.,1.],speed_factor=1.5)
        
    def ship_loc(self):
        return np.array(self.map.ship.location)        
        
    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, key_str = keycode
        print key
        if key in (9, 13) and self.next is not None:
            self.next.focus = True
            self.next.select_all()
        else:
            super(TabTextInput, self)._keyboard_on_key_down(window, keycode, text, modifiers)    
        
    def touch(self):
        self.touched = True
        if self.touch_event is not None:
            self.touch_event.cancel()
        self.touch_event = Clock.schedule_once(self.reset_touch,1)
        if self.anim: self.anim.cancel(self)
    
    def reset_touch(self,*args):
        self.touch_event = None
        self.touched = False
        self.reset_camera()
                
class MapScatterPlane(ScatterPlane):
    
    def __init__(self,**kwargs):
        super(MapScatterPlane,self).__init__(**kwargs)                
        self.trans = None
        self.scale_anim = False
        
    def on_transform_with_touch(self,touch):
        self.propagate_scale()
        self.parent.touch()                   
        
    def propagate_scale(self,*args):
        for c in self.children:
            if hasattr(c,'on_mapscale'): c.on_mapscale(self)    
        
    def on_touched(self,touch):        
        self.parent.touch()              
        return False
               
    def on_scale(self,*args):
        self.propagate_scale()           
    
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
        
    



