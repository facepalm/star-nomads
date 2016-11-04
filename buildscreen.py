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
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix, Translate
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import math

import globalvars
import gps
import starfield
import numpy as np
import util
from functools import partial


kv = '''
<BuildScreen@Screen>:
    name: 'Build screen'
    
'''

Builder.load_string(kv)

class BuildScreen(Screen):
    location = ListProperty([0, 0])
    
    def __init__(self,**kwargs):     
        Screen.__init__(self,**kwargs) 
        self.location = kwargs['location']
        
        

