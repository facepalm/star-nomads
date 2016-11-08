from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import ScatterPlane
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix, Translate, Rectangle, Canvas
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout

import math

import globalvars
import gps
import starfield
import numpy as np
import util
from functools import partial

from listscreen import ListScreen, ListScreenEntry

        

class BuildScreen(ListScreen):
    
    def __init__(self,**kwargs):     
        if 'name' not in kwargs: kwargs['name'] = 'Build Screen'
        ListScreen.__init__(self,**kwargs)         
        
        testLbl = ListScreenEntry()
        testLbl.addText('Test of label text')
        testLbl.addText('Test line 2')
        testLbl.addText('Test line 3')
        
        self.ids['entries'].add_widget(testLbl)
        

