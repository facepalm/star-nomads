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
from kivy.uix.button import Button
from kivy.metrics import Metrics


import numpy as np


import shipimage
import util


kv = '''
<ShipScreen@Screen>:
    name: 'ark screen'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
           
    
    ScrollView:
        id: shipscroll
               
        pos_hint: {'center_x': .5, 'center_y': .5}
                                                                         
            
        FloatLayout:
            id: shiplayout  
            size: (800, 3520)
            size_hint: None, None 
            #Image:
 
<RoomImage@Image>:
    size: '40dp','40dp'
    size_hint: None, None     
    
    Image:
        id: roomicon
        size: '30dp','30dp'
        size_hint: None, None 
        mipmap: True
    
    Image:
        id: sizeimg
        size: '20dp','20dp'
        size_hint: None, None
                           
'''

Builder.load_string(kv)

def densFix(coords):
    return (np.array(coords) * Metrics.density).tolist()

class RoomImage(Image):
    def __init__(self, **kwargs):
        self.room = kwargs['room']
        self.rsize = kwargs['rsize']
        if self.room: 
            self.source = 'img/icon/modules/filled-generic.png'
        else:
            self.source = 'img/icon/modules/empty-generic.png'
        Image.__init__(self,**kwargs)
        
        self.ids['roomicon'].source = self.room.img_dict['icon'] if self.room else 'img/icon/modules/blank.png'
        self.ids['roomicon'].color = self.room.img_dict['icon color'] if self.room else [0.8,0.8,0.8,1]
        
        self.ids['sizeimg'].source = ''.join(['img/icon/modules/',str(self.rsize),'.png'])
        if self.room and not self.room.img_dict['displaysize']: self.ids['sizeimg'].color = [1,1,1,0]
        self.sizeoffset = self.room.img_dict['sizeloc'] if self.room else [0, 0]
        #loc = self.room.img_dict['sizeloc'] if self.room else [0.5, 0.5]
        #self.ids['sizeimg'].pos_hint = loc 
        
        '''self.background_color = [0.3,0.3,0.3,1.0]
        if self.room:
            self.background_color = [0.8,0.8,0.8,1.0] #TODO room symbols
            if self.room.active:
                self.background_color = [0.2,1.0,0.2,1.0] #TODO edit of room symbol'''
                
        self.refresh()                
                
    def go_to_loc(self,loc):
        self.center = loc
        self.ids['sizeimg'].center = (np.array(loc)+np.array(self.sizeoffset)).tolist()
        self.ids['roomicon'].center = loc
        
    def refresh(self):
        self.color = self.room.color if self.room else [1,1,1,1]                   

class ShipScreen(Screen):
    def __init__(self,**kwargs):
        super(ShipScreen,self).__init__(**kwargs)
        
        self.ship = kwargs['ship'] #TODO catch errors if missing
        #print shipimage.ship_dict,self.ship.shipclass,'prefix', '/ShipRoomsRotate.png'
        
        
        
        
    def on_pre_enter(self):
        interior_img = Image(source=shipimage.ship_dict[self.ship.shipclass]['prefix']+ '/ShipRooms.png',color=[0.5,0.5,0.5,1.], allow_stretch=True, size_hint= [None, None])
        interior_img.size = densFix(interior_img.texture.size)
        interior_img.pos_hint= {'center_x': .5, 'center_y': .5}
        self.ids['shiplayout'].add_widget(interior_img)
        self.ids['shiplayout'].size = (np.array(interior_img.size)+100).tolist()
        
        #add rooms
        for r in self.ship.rooms:
            #mimg = r['module'].module_image()
            rimg = RoomImage(room = r['module'], rsize = r['size'])
            #butt.text = str(r['size'])
            #room_name = 'room'+str(r['size'])+'_'
            #room_name += 'empty.png' if not r['module'] else 'full.png'
            b_center = np.array(self.ids['shiplayout'].center)+np.array(r['loc'])*Metrics.density        
            #print r_center, np.array(self.ids['shiplayout'].center),np.array(r['loc'])       
            #room_img = Image(source='img/room/'+room_name, center = r_center.tolist(), size=[40,40], size_hint= [None, None])
            #rimg.center = b_center.tolist()
            rimg.go_to_loc(b_center.tolist())
            #rimg.ids['sizeimg'].pos_hint = 0.5,0.5
            self.ids['shiplayout'].add_widget(rimg)
            
        self.ids['shipscroll'].scroll_x = 0.5
        self.ids['shipscroll'].scroll_y = 0.5
        
        #add panels
        #add status
        
    def on_leave(self):  
        self.ids['shiplayout'].clear_widgets()               
        
