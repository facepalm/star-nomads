import kivy
kivy.require('1.9.1')

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock


import globalvars
import util
import gps
import game

kv = '''
<MenuScreen@Screen>:
    name: 'game menu'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
    
    BoxLayout:
        size_hint: 0.8,0.8
        pos_hint: {'center_x': 0.5, 'center_y': .5}
        padding: 20
        spacing: 10
        orientation: 'vertical'
        
        Button:
            text: 'New Game'
            on_press: self.parent.parent.on_newgame_button()
        Button:
            text: 'Save & Quit'
            on_press: self.parent.parent.on_savequit_button()
'''

Builder.load_string(kv)

class MenuScreen(Screen):
    pass
    
    def on_newgame_button(self,*args):
        print 'New game!'
        globalvars.root.initialize()
        gps.hard_reset()
        globalvars.universe = game.Universe()
        Clock.schedule_interval(globalvars.universe.update, 1./1.)
        util.autosave()
        

    def on_savequit_button(self,*args):
        print 'Saving and quitting'
        util.autosave()
        quit()
