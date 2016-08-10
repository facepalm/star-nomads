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
        
        super(EventMapImage, self).__init__(**kwargs)
        
        self.size = [self.texture.size[0]/20, self.texture.size[1]/20]
        print self.size
        
        self.color = self.event.color
        self.center = self.event.location.tolist()
        
        self.opacity = 1 if self.event.discovered else 0
                
