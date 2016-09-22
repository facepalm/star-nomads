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

import globalvars

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
        Button:
            text: 'Save & Quit'
'''

Builder.load_string(kv)

class MenuScreen(Screen):
    pass

