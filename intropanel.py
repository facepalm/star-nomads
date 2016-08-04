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

import globalvars

class ScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollView, self).__init__(**kwargs)
           
        with self.canvas.before:
            self.color = Color(0.20,0.20,0.20)
            self.rect = Rectangle(pos=self.pos, size=self.size)
    
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)

kv = '''
<IntroPanel>:

'''

class IntroPanelView(Screen):
    introtext = '''[color=aaaaaa]
[size=10]-~- No autosave found.  Initializing new game -~-[/size][color=ffffff]     
   
Gobbo intro.[/color]
    '''

    def __init__(self, **kwargs):
        super(IntroPanelView, self).__init__(**kwargs)
        self.name='introscreen' 
        
        # create a default grid layout with custom width/height
        layout = GridLayout(cols=1, padding=10, spacing=10,
                size_hint=(None, None),pos_hint={'center_x': .5, 'center_y': .5}, width=500)
        
        layout.bind(minimum_height=layout.setter('height'))

        # create a scroll view, with a size < size of the grid
        scrl = ScrollView(size_hint=(None, None), size=(500, 320),
                pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        
        label = Label(
            text=self.introtext,
            size=(480, 900),
            text_size=(480,900),
            size_hint_y=None,
            markup=True)
        
        scrl.add_widget(label)
        layout.add_widget(scrl)
        
        btn = Button(text='Okay', size=(480, 40),
                         size_hint=(None, None), on_press=self.close)
        
        layout.add_widget(btn)
        
        self.add_widget(layout)
        
    def close(self, instance):
        globalvars.root.onBackBtn()
  

