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


kv = '''
<BuildScreen@Screen>:
    name: 'Build screen'
    
    ScrollView:
        
    
        StackLayout:
            size_hint: 1.0, None
            id: entries
            
            canvas.before:
                Color:
                    rgb: 0.2, 0.2, 0.2
                Rectangle:
                    pos:  self.pos
                    size: self.size
        
        
                
<ListScreenEntry@StackLayout>:
    id: items
    orientation: 'tb-lr'
    padding: 5,5,5,5

    #horizontal bar
            

    canvas.before:
        Color:
            rgb: 0.1, 0.1, 0.1            
        Rectangle:
            pos:  self.pos
            size: self.size
            
    canvas.after:
        Color:
            rgb: 0.5, 0.5, 0.5            
        Rectangle:
            pos:  self.pos
            size: self.width, dp(5)     
                                  
'''

Builder.load_string(kv)

class ListScreenEntry(StackLayout):
    verticality = NumericProperty(0)    
    def addText(self,text=''):
        newtext = Label(text=text,markup=True, size_hint= (1.0,None) )
        newtext.height = 15
        self.add_widget(newtext)

        self.verticality += newtext.height
        self.size = (Window.width,self.verticality)        
        print self.size, self.minimum_size
        
        

class BuildScreen(Screen):
    location = ListProperty([0, 0])
    
    def __init__(self,**kwargs):     
        Screen.__init__(self,**kwargs) 
        self.location = kwargs['location']

        hdrLbl = ListScreenEntry()
        hdrLbl.addText('[b]TITLE OF PAGE[/b]')
        self.ids['entries'].add_widget(hdrLbl)
        
        testLbl = ListScreenEntry()
        testLbl.addText('Test of label text')
        testLbl.addText('Test line 2')
        testLbl.addText('Test line 3')
        
        self.ids['entries'].add_widget(testLbl)
        

