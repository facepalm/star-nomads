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
 
<RoomButton@Button>:
    size: '40dp','40dp'
    size_hint: None, None     
                           
'''

Builder.load_string(kv)

def densFix(coords):
    return (np.array(coords) * Metrics.density).tolist()

class RoomButton(Button):
    pass

class ShipScreen(Screen):
    def __init__(self,**kwargs):
        super(ShipScreen,self).__init__(**kwargs)
        
        self.ship = kwargs['ship'] #TODO catch errors if missing
        #print shipimage.ship_dict,self.ship.shipclass,'prefix', '/ShipRoomsRotate.png'
        interior_img = Image(source=shipimage.ship_dict[self.ship.shipclass]['prefix']+ '/ShipRooms.png',color=[0.2,0.2,0.2,1.], allow_stretch=True, size_hint= [None, None])
        interior_img.size = densFix(interior_img.texture.size)
        interior_img.pos_hint= {'center_x': .5, 'center_y': .5}
        self.ids['shiplayout'].add_widget(interior_img)
        self.ids['shiplayout'].size = (np.array(interior_img.size)+100).tolist()
        
        #add rooms
        for r in self.ship.rooms:
            butt = RoomButton()
            butt.text = str(r['size'])
            #room_name = 'room'+str(r['size'])+'_'
            #room_name += 'empty.png' if not r['module'] else 'full.png'
            b_center = np.array(self.ids['shiplayout'].center)+np.array(r['loc'])*Metrics.density        
            #print r_center, np.array(self.ids['shiplayout'].center),np.array(r['loc'])       
            #room_img = Image(source='img/room/'+room_name, center = r_center.tolist(), size=[40,40], size_hint= [None, None])
            butt.center = b_center.tolist()
            self.ids['shiplayout'].add_widget(butt)
            
        self.ids['shipscroll'].scroll_x = 0.5
        self.ids['shipscroll'].scroll_y = 0.5
        
        #add panels
        #add status
        
