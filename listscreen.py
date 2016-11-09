from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
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
<ListScreen@Screen>:
    name: 'List screen'
    
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

    size_hint: None, None
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

class MultiLineLabel(Label):
    def __init__(self, **kwargs):
        super(MultiLineLabel, self).__init__( **kwargs)
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = self.texture_size[1]
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)

class ListScreenEntry(StackLayout):
    verticality = NumericProperty(10)    
    
    def addText(self,text=''):
        newtext = Label(text=text,markup=True, size_hint= (1.0,None) )
        newtext.texture_update()
        newtext.size = newtext.texture_size
        self.add_widget(newtext)

        self.verticality += newtext.height
        self.size = (Window.width,self.verticality)        
        print self.size
        
    def addButton(self,text='',btntxt = '',callback=None):
        entrysize = [0,0]
        horiz = RelativeLayout(size_hint= (1.0,None))#orientation = 'lr-tb',padding=(5,5,5,5))
        
        newtext = Label(text=text,markup=True, size_hint= (1.0,None) )
        newtext.texture_update()
        newtext.size = newtext.texture_size
        newtext.size_hint = (None,None)
        entrysize = [ entrysize[0] + newtext.width , max(entrysize[1],newtext.height) ]        
        
        #horiz.center = (Window.width/2,-entrysize[1]/2)
        #(Window.width/2-entrysize[0]/2-5, -entrysize[1]/2) #- newtext.width
        
        
        btn = Button(text=btntxt)
        if callback is not None: btn.bind(on_press=callback)
    
        btn.size_hint = (None,None)
        btn.texture_update()
        btn.size = btn.texture_size
        print newtext.size, btn.size
        btn.width += 10
        btn.height += 10
        entrysize = [ entrysize[0] + btn.width , max(entrysize[1], btn.height) ]

        horiz.size=(entrysize[0],entrysize[1]+7)
        btn.center = (Window.width/2 + btn.width/2+5, btn.height/2+5) #- newtext.width                
        newtext.center = (Window.width/2 - newtext.width/2-5,btn.height/2+5)#(Window.width/2-newtext.width/2-5,-entrysize[1]/2)
        #horiz.size = (entrysize[0], entrysize[1])


        print entrysize
        #horiz.center = (Window.width/2,-entrysize[1]/2)
        
        horiz.add_widget(newtext)
        horiz.add_widget(btn)       
                              
        self.verticality += entrysize[1]+7
        self.size = (Window.width,self.verticality)        
        self.add_widget(horiz)

        print self.verticality        

class ListScreen(Screen):
    location = ListProperty([0, 0])
    
    def __init__(self,**kwargs):     
        Screen.__init__(self,**kwargs) 
        self.location = kwargs['location']
        self.name = kwargs['name']

        ttlLbl = ListScreenEntry()
        
        ttlLbl.addText('[size=24]'+str(self.name)+'[/size]')
        self.ids['entries'].add_widget(ttlLbl)
        
        
        '''testLbl = ListScreenEntry()
        testLbl.addText('Test of label text')
        testLbl.addText('Test line 2')
        testLbl.addText('Test line 5')
        
        testLbl.addButton('Test btn:','press!',None)
        
        testLbl.addText('Test line 4')
        
        self.ids['entries'].add_widget(testLbl)'''
        

