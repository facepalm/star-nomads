from kivy.uix.image import Image
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix

import numpy as np

import globalvars

#manager for ship images & icons
ship_dict = {   'Ark': {'prefix':'img/ark/', 'coords':[26,41]},
                'Station' : '',
                'Capital' : '',
                'Generic' : ''
                }


class ShipImage(Image):
    pressed     = ListProperty([0, 0])       
    coords      = ListProperty([0, 0])
    bearing     = NumericProperty(90)
       
    def __init__(self,**kwargs):
        self.ship = kwargs['ship'] 
        if self.ship:   
            self.source = ship_dict[self.ship.shipclass]['prefix']+ '/MapSymbolSmall.png'
        #print self.source, self.ship.shipclass
            
        super(ShipImage, self).__init__(**kwargs)
        
        self.size = [self.texture.size[0]/2, self.texture.size[1]/2]
        
        self.rotation = None
        
        self.coords = self.ship.get_location()
        
        self.place_image()
        
        self.center = [0,0]
        
        if self.ship.faction == 'Player':
            self.color = [0,0.9,0.1,1]

    def on_touch_down(self, touch):
        touch.push()
        print touch.pos
        touch.apply_transform_2d(self.to_parent)
        touched = self.collide_point(*touch.pos)
        print self.center, touch.pos
        touch.pop()
        if touched:
            self.pressed = touch.pos
            print "ship pressed"
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return False
        return super(ShipImage, self).on_touch_down(touch)

    def on_coords(self,*args):
        self.center = self.coords

    def on_pressed(self, instance, pos):
        print ('Ship ',self.ship.shipclass,', pressed at {pos}'.format(pos=pos))
        #print self.planet.type, self.planet.resources.raw, self.planet.subtype if hasattr(self.planet,'subtype') else ''
        print globalvars.root
        
        '''pname = util.short_id(self.planet.id)+'-planet'
        if not globalvars.root.screen_manager.has_screen(pname):
            p = planetview.PlanetPanel(planet=self.planet)
            globalvars.root.screen_manager.add_widget( p )
        globalvars.root.onNextScreen(pname)'''


    def place_image(self):        
        #self.pos = [self.coords[1] * globalvars.config['MAP SCALING'], self.coords[0] * globalvars.config['MAP SCALING']]       
                     
        if self.rotation:
            self.rotation.angle = -self.bearing
            self.rotation.origin = np.array(self.texture.size)/2        
        else:
            with self.canvas.before:
                PushMatrix()
                       
                ph = self.pos
                x = ph[0]
                y = ph[1]
                 
                
                self.rotation = Rotate(angle= -self.bearing, origin = (0,0) )#- np.array(ship_dict[self.ship.shipclass]['coords'])) 
                print self.pos,  self.rotation.origin
                
            with self.canvas.after:
                
                #self.occupied_indicator = [Color( 0.5, 0.5, 0.5, 0.5 ), Line(circle=( 2000*x,2000*y, 20), width=3)]
                PopMatrix()                                       
                     
                        
                      
        
