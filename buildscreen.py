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
from functools import partial

import globalvars
import gps
import starfield
import numpy as np
import util
from functools import partial
import ship

from listscreen import ListScreen, ListScreenEntry




class BuildScreen(ListScreen):
    
    def __init__(self,**kwargs):     
        if 'name' not in kwargs: kwargs['name'] = 'Build Screen'
        self.location = kwargs['location']
        ListScreen.__init__(self,**kwargs)         
        
        testLbl = ListScreenEntry()
        testLbl.addText('Lichen station')
        testLbl.addText('Built of scraps and spares, lichens are the most tenacious and adaptable station type, capable of accomodating a little bit of everything as needed.')
        testLbl.addText('Cost: <calculate costs>')
        
        testLbl.addButton('Build this station:','BUILD',partial(self.build_ship,'LICHEN'))
        
        self.ids['entries'].add_widget(testLbl)
        
        testLbl = ListScreenEntry()
        testLbl.addText('Generic Orbital station')
        testLbl.addText('Built of yadda yadda yadds')
        testLbl.addText('Cost: <calculate costs>')
        
        testLbl.addButton('Build this station:','BUILD',partial(self.build_ship,'GENERIC_STATION'))
        
        
        self.ids['entries'].add_widget(testLbl)

    def build_ship(self,shiptype,caller=None):
        built = True
        if shiptype == 'LICHEN':
            globalvars.map.spawn( ship.Lichen(location = self.location), self.location )
        elif shiptype == 'GENERIC_STATION':
            globalvars.map.spawn( ship.Station(location = self.location), self.location )
        else:
            built=False
        if built:
            #return to map screen
            self.close()

    def close(self, instance=None):
        globalvars.root.onBackBtn(remove=True)                        

