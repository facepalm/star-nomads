from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty

kv = '''
<GalaxyScreen@Screen>:
    name: 'galaxy map'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
    reload_needed: True
           
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
    reload_needed = BooleanProperty()

    def __init__(self,**kwargs):
        super(GalaxyScreen,self).__init__(**kwargs)
        self.universe = kwargs['universe']
            
