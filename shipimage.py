from kivy.uix.image import Image
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix
from kivy.animation import Animation

import numpy as np

import globalvars

#manager for ship images & icons
ship_dict = {   'Ark': {'prefix':'img/ark/', 'style':{'Generic':'MapShip.png'}, 'coords':[26,41]},
                'Station' : {'prefix':'img/icon/noun-project/', 'style':{'Generic':'focus-lab-space-station.png', 'Lichen':'oliviu-stoian-station.png'}, 'coords':[25,25]},
                'Capital' : '',
                'Generic' : ''
                ''
                }


class ShipImage(Image):
    pressed     = ListProperty([0, 0])       
    coords      = ListProperty([0, 0])
    bearing     = NumericProperty(45)
       
    def __init__(self,**kwargs):
        self.ship = kwargs['ship'] 
        if self.ship and 'source' not in kwargs:   
            self.source = ship_dict[self.ship.shipclass]['prefix']+ ship_dict[self.ship.shipclass]['style'][self.ship.style]

        #print self.source, self.ship.shipclass
        kwargs['mipmap'] = True
        super(ShipImage, self).__init__(**kwargs)
        
        self.initialized = False
        
        self.size = [20,30]#[self.texture.size[0]/2, self.texture.size[1]/2]
        self.orig_size = [20,30]
        
        self.rotation = None
        
        self.coords = self.ship.get_location()  #will place image at correct position    
                
        #self.center = self.coords#[0,0]
        
        #print 'coordscoordscoords',self.coords
        #self.place_image()                
        
        if self.ship.faction == 'Player':
            self.color = [0,0.9,0.1,1]
            
        self.initialized = True
        self.allow_stretch = True

        self.map = globalvars.map
        
    def on_mapscale(self,mapscale=None):
        self.size = (np.array(self.orig_size)*min(4.,2./mapscale.scale)).tolist()
        self.center = self.center
        self.on_coords(self.coords, instant=True)

    def on_touch_down(self, touch):
        return False
        touch.push()
        #print touch.pos
        #print 'parent',self.to_window(touch.pos[0],touch.pos[1],relative=True)
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)
        #print self.center, touch.pos
        touch.pop()
        if touched:
            self.pressed = touch.pos
            self.ship.touched()
            print "ship pressed"
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return False
        return super(ShipImage, self).on_touch_down(touch)

    def on_coords(self,*args,**kwargs):
        instant = kwargs['instant'] if 'instant' in kwargs else False
        if self.initialized and not instant:
            self.place_image()   
            anim = Animation(center = [self.coords[0],self.coords[1]], duration=1.)
            anim.start(self)
            anim = Animation(origin = [self.coords[0],self.coords[1],0.0], duration=1.)
            anim.start(self.rotation)
            pass
        else:
            self.center = self.coords
            self.place_image()             
        
    def on_bearing(self,*args):        
        self.place_image()

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
            self.rotation.origin = self.center
            
        else:
            with self.canvas.before:
                PushMatrix()
                       
                ph = self.center
                x = ph[0]
                y = ph[1]
                 
                
                self.rotation = Rotate(angle= -self.bearing, origin = self.center )
                print self.pos,  self.rotation.origin
                
            with self.canvas.after:
                
                #self.occupied_indicator = [Color( 0.5, 0.5, 0.5, 0.5 ), Line(circle=( 2000*x,2000*y, 20), width=3)]
                PopMatrix()                                       
                pass
                        
                      
        
