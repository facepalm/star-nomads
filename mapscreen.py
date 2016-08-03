from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.app import App

import globalvars

kv = '''
<MapScreen@Screen>:
    name: 'star map'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
    
    Scatter:
        id: mapscale
        index: 0
        pos: 0,0
        do_collide_after_children: True
        auto_bring_to_front: False
        do_rotation: False
        
        Label:
            pos_hint: {'center_x': 0.5, 'center_y': .5}
            text: 'test'                      
    FloatLayout:
        id: mapoverlay  
        index: 5 
        Button: 
            pos_hint: {'top': 0.50, 'right': 0.50}
            size_hint: 0.15,0.15
            text: 'Build'
'''

Builder.load_string(kv)

class MapScreen(Screen):
    def __init__(self,**kwargs):
        super(MapScreen,self).__init__(**kwargs)
        
        
    
    



