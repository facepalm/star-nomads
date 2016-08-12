from kivy.uix.image import Image
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix

import numpy as np

import globalvars

class EventMapImage(Image):
    pressed     = ListProperty([0, 0])       
    coords      = ListProperty([0, 0])
    
    def __init__(self,**kwargs):
        self.event = kwargs['event']
        self.source = 'img/event/'+self.event.category+'/MapSymbol.png'
        #self.allow_stretch=True
        super(EventMapImage, self).__init__(**kwargs)
        
        self.size = [10,10]
        
        self.color = self.event.color
        self.center = self.event.location.tolist()
        
        self.opacity = 1 if self.event.discovered else 0
        
    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)
        touch.pop()
        if touched and self.opacity > 0:
            self.pressed = touch.pos
            print "Event pressed"
            self.event.on_pressed()
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return False
        return super(EventMapImage, self).on_touch_down(touch)     

    def suicide(self):
        if self.parent:
            self.parent.remove_widget(self)           
        
        
                
