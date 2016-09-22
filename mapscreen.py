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

PING_SPEED = 50.

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
        mapxy: self.parent.location[1]+self.parent.width/2,self.parent.location[0]+self.parent.height/2
        
        Image:
            size: 1,1
            color: 1,0,0,1
            center: self.parent.parent.location
        
      
                                                                                 
            
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
            Image:
                mipmap: True
                size_hint: 0.1, 0.1
                pos_hint: {'x': 0.0, 'left': 1.00}
                id: systemposition
                source: 'img/icon/sun.png'
                color: 1.0, 0.95, 0.05, 1.0
                
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
                id: warehousebtn   
                on_press: self.parent.parent.parent.on_respanel_button()             
                BoxLayout:
                    pos: self.parent.pos
                    size: self.parent.size
                    
                    Image:
                        source: 'img/icon/noun-project/victor-fedyuk-clipboard.png'
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
                size_hint: 0.5, 1.0
                text_size: self.size[0]*0.9, self.size[1]*0.9
                halign: 'left'
                valign: 'middle'
                text:"Test text doo doo de doo tjlkasldkjadl\\n fhjklhdzfk jhzdslkf"                                                       
                    
                        
            
    StackLayout:  
        id: debugoverlay  
        orientation: 'tb-lr' 
        Label:
            pos_hint: {'top': 1.00, 'left': 0.2}
            size_hint: 0.5,0.05
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
        self.map = kwargs['map'] if 'map' in kwargs else None
        super(MapScreen,self).__init__(**kwargs)
        
        self.name = 'Star Map -'+util.short_id(self.map.id)
        
        self.Builder = None
        
        self.displayed = False
        self.curr_loc = [0,0]
        
        self.ids['stars'].density = 500./self.map.density
        self.ids['stars'].on_size()
        
    def on_shippanel_button(self):
        if self.map and self.map.ship:
        
            self.map.ship.touched()        
        
    def on_respanel_button(self):
        if self.map and self.map.ship:
            globalvars.root.switchScreen(self.map.ship.storage.get_screen())   
            
    def on_galmappanel_button(self):
        globalvars.root.switchScreen(self.map.universe.galaxy_map)      
        
    def on_pre_enter(self):
        gps.start()
        self.displayed = True
        
        min_side = min(Window.width, Window.height)
        globalvars.config['MAP SCALING'] = (min_side - 200)/200.
        self.ids['mapscale'].scale = globalvars.config['MAP SCALING']
        print 'Resolution information:',Window.width, Window.height, globalvars.config['MAP SCALING']
        
        #Clock.schedule_interval(self.update, 0.1)               
                
    def on_leave(self):  
        self.displayed = False              
        gps.stop()
        
    def update(self,dt):
        #self.location = gps.get_location()
        self.ids['gpslabel'].text = 'ON' if gps.use_gps else 'OFF'
        self.ids['mapscale'].touched=False  
        return self.displayed
        
    def on_location(self, *args):
        dx = self.location[0] - self.curr_loc[0] 
        dy = self.location[1] - self.curr_loc[1]
        
        dist = math.sqrt(dx**2 + dy**2)
        animate = False if self.curr_loc == [0,0] or dist >= 10000 else True
        print "animate", animate, self.curr_loc, dist
        self.ids['stars'].animation = animate
        
        self.curr_loc = self.location
        self.ids['stars'].shift(dx,dy)
        #print self.ids['stars'].scale
        self.ids['stars'].scale = 0.001*globalvars.config['MAP SCALING']*self.ids['mapscale'].scale
        
        #print 'map',self.ids['mapscale'].mapxy
        self.ids['mapscale'].mapxys = [-self.ids['mapscale'].scale*self.location[0] + self.width/2,-self.ids['mapscale'].scale*self.location[1] + self.height/2, self.ids['mapscale'].scale]
        
        #self.ids['mapscale'].x = -globalvars.config['MAP SCALING']*self.location[0] + self.width/2 #dx*2#globalvars.config['MAP SCALING']
        #self.ids['mapscale'].y = -globalvars.config['MAP SCALING']*self.location[1] + self.height/2#dy*2#globalvars.config['MAP SCALING']
        
        duration = 1.0 if animate else 0.01
        if not self.ids['mapscale'].touched:
            anim = Animation( pos = [-globalvars.config['MAP SCALING']*self.location[0] + self.width/2,-globalvars.config['MAP SCALING']*self.location[1] + self.height/2], duration = duration )#, t='in_out_sine')        
            anim &= Animation( scale = globalvars.config['MAP SCALING'], duration = duration)       
            anim.start(self.ids['mapscale'])
            
        #self.ids['mapscale'].update_mapxy()
        
        #print Clock.time()
        #print self.ids['mapscale'].x, self.ids['mapscale'].y
        
        sys = self.map.which_system(self.location)
        
        #if sys is None:
            #we're in deep space
        self.ids['systemposition'].source= ''
        self.ids['systemposition'].color = [0.,0.05,0.1,1.0]
        if sys is not None:
            pos = sys.proximity(self.location)
            if pos == 'Near star':
                self.ids['systemposition'].source = 'img/icon/fire.png'
                self.ids['systemposition'].color  = [1.0, 0.5, 0.05, 1.0]
            elif pos == 'Goldilocks': #TODO find a good planetary symbol
                self.ids['systemposition'].source = 'img/icon/sun.png'
                self.ids['systemposition'].color  = [0.5, 0.95, 0.05, 1.0]
            elif pos == 'Inner system':
                self.ids['systemposition'].source = 'img/icon/sun.png'
                self.ids['systemposition'].color  = [1.0, 0.95, 0.05, 1.0]
            elif pos == 'Outer system':
                self.ids['systemposition'].source = 'img/icon/snowflake.png'
                self.ids['systemposition'].color  = [0.75, 0.75, 0.95, 1.0]
            elif pos == 'Kuiper belt':
                self.ids['systemposition'].source = 'img/icon/icecube.png'
                self.ids['systemposition'].color  = [0.5, 0.5, 0.95, 1.0]
        
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
        
    #    print args
    #    print 'loc changed!'        
                
class MapScatterPlane(ScatterPlane):
    mapxys = ListProperty([0,0,1])
    
    def __init__(self,**kwargs):
        super(MapScatterPlane,self).__init__(**kwargs)                
        self.trans = None
        self.update_mapxy()
        self.touched = False
        
    def on_transform_with_touch(self,touch):
        self.touched = True           
        
    def on_touched(self,touch):
        self.touched = True   
        return False
    
    '''    
    #from https://github.com/kivy/kivy/wiki/Menu-on-long-touch    
    def menu(self, touch, *args):
        menu = BoxLayout(
                size_hint=(None, None),
                orientation='vertical',
                center=touch.pos)
        menu.add_widget(Button(text='a'))
        menu.add_widget(Button(text='b'))
        close = Button(text='close')
        close.bind(on_release=partial(self.close_menu, menu))
        menu.add_widget(close)
        self.parent.add_widget(menu)    
        
    def close_menu(self, widget, *args):
        self.parent.remove_widget(widget)        
        
    def create_clock(self, touch, *args):
        callback = partial(self.menu, touch)
        Clock.schedule_once(callback, 1)
        touch.ud['event'] = callback

    def delete_clock(self, touch, *args):
        if 'event' in touch.ud: Clock.unschedule(touch.ud['event'])    
        
    def on_touch_down(self,*args):
        self.create_clock(*args)
        return False
    
    def on_touch_up(self,*args):
        self.delete_clock(*args)
        return False   '''
        
        
        
    def update_mapxy(self,*args): 
        self.touched=False  
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
        
    



