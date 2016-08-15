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


import shipimage
import util

kv = '''
<ShipScreen@Screen>:
    name: 'ark screen'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
           
    
    ScrollView:
        id: shipscroll
        size_hint: None, None
        size: (500, 320)
        pos_hint: {'center_x': .5, 'center_y': .5}
                                                                         
            
        FloatLayout:
            id: shiplayout  
            #Image:
                           
'''

Builder.load_string(kv)

class ShipScreen(Screen):
    def __init__(self,**kwargs):
        super(ShipScreen,self).__init__(**kwargs)
        
        self.ship = kwargs['ship'] #TODO catch errors if missing
        #print shipimage.ship_dict,self.ship.shipclass,'prefix', '/ShipRoomsRotate.png'
        room_img = Image(source=shipimage.ship_dict[self.ship.shipclass]['prefix']+ '/ShipRoomsRotate.png',color=[0.2,0.2,0.2,1.])
        self.ids['shiplayout'].add_widget(room_img)
        
        #add rooms
        #add panels
        #add status
        
