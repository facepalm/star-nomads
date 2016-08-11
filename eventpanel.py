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
        self.pos = self.event.location.tolist()
        
        self.opacity = 1 if self.event.discovered else 0
                
