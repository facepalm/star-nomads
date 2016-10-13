from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivy.graphics import Line, Color, PushMatrix, PopMatrix
from kivy.core.window import Window

import globalvars

kv = '''
<GalaxyScreen@Screen>:
    name: 'galaxy map'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
    refresh_needed: True
           
    ScatterPlane:
        id: galplane
        screen: self.parent
        index: 0
        scale: 2.
        pos: 0,0#self.parent.width/2,self.parent.height/2
        do_collide_after_children: True
        auto_bring_to_front: False
        do_rotation: False
        #mapxy: self.parent.location[1]+self.parent.width/2,self.parent.location[0]+self.parent.height/2
        
        Image:
            size: 1015,1022
            source: 'img/galaxy/m100_apod_JudySchmidt_CC3/m100_hubble_4060-downsampled.png'
            pos: 0,0
            '''
Builder.load_string(kv)

class GalaxyScreen(Screen):
    refresh_needed = BooleanProperty()

    def __init__(self,**kwargs):
        super(GalaxyScreen,self).__init__(**kwargs)
        self.universe = kwargs['universe']
        
    def refresh(self,*args):        
        plane = self.ids['galplane']
        plane.canvas.after.clear()
                
        plane.canvas.after.add(Color(1,0.1,0.1,1))
        for m in self.universe.map_nodes:
            coords = self.universe.map_nodes[m]['Map'].galactic_coordinates
            dot = Line(circle=(coords[0],coords[1],2),width=2)
            plane.canvas.after.add(dot)
            
        plane.canvas.after.add(Color(1,.9,0.1,1))
        if globalvars.map:
            coords = globalvars.map.galactic_coordinates
            dot = Line(circle=(coords[0],coords[1],1),width=1.5)
            plane.canvas.after.add(dot)
            plane.pos = [-plane.scale*coords[0] + Window.width/2,-plane.scale*coords[1] + Window.height/2]
                            
        plane.canvas.after.add(Color(1,1,1,1))            
