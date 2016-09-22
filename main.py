import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window  
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SwapTransition, SlideTransition
from kivy.lang import Builder

from intropanel import IntroPanelView
import util
import globalvars
import game
import gps
import menuscreen

#graphics stuff

Builder.load_string("""
<GameRoot>:  
    screen_manager: screen_manager
    ScreenManager:
        id: screen_manager
        """)


class GameRoot(AnchorLayout):  
    #blatantly swiped from http://www.pygopar.com/kivys-screenmanager-and-back-button/
    """ Root widget for app """
    screen_manager = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(GameRoot, self).__init__(*args, **kwargs)
        self.list_of_prev_screens = []

    def onNextScreen(self, next_screen, transition='None'):
        if transition == 'None':
            self.screen_manager.transition = NoTransition()  
        else:
            self.screen_manager.transition = SlideTransition()
        if not self.list_of_prev_screens or (self.list_of_prev_screens[-1] is not self.screen_manager.current):
            self.list_of_prev_screens.append(self.screen_manager.current)
        self.screen_manager.current = next_screen
        
    def onBackBtn(self):
        if self.list_of_prev_screens:
            curr = self.screen_manager.current
            self.screen_manager.current = self.list_of_prev_screens.pop()
            if not self.list_of_prev_screens:
                self.list_of_prev_screens.append(curr)
            return True
        return False
        
    def switchScreen(self,next_screen, transition='Slide'):
        if not self.screen_manager.has_screen(next_screen.name):
            self.screen_manager.add_widget( next_screen )
        self.onNextScreen(next_screen.name)        
        
    def initialize(self):
        self.screen_manager.clear_widgets()
        self.list_of_prev_screens = []
        menu = menuscreen.MenuScreen()
        self.switchScreen(menu)
                    
        
    #def hideScreen(self,screen):
    #    if not self.screen_manager.has_screen(screen.name):
    #        self.screen_manager.add_widget( screen )
    #    self.list_of_prev_screens.append(screen.name)

class GameApp(App):

    def __init__(self, **kwargs):
        super(GameApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.onBackBtn)

    def on_pause(self,*args):
        print "Pausing!"
        gps.stop()
        return True
        
    def on_resume(self):
        print "Resuming!"
        pass

    def onBackBtn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc key """
        # 27 is back press number code
        if key == 27:
            return globalvars.root.onBackBtn()
        return False

    def build(self):
        root = GameRoot()
        globalvars.root = root
        #menu = menuscreen.MenuScreen()
        globalvars.root.initialize()
        autoloaded = util.autoload() if globalvars.config['AUTOLOAD'] else False
        
                
        if not autoloaded:            
            #generate universe
            
            globalvars.universe = game.Universe()
            #root.screen_manager.add_widget( IntroPanelView() )
            #root.onNextScreen('introscreen','None')            
            #autosave?
            util.autosave()
            
        
        
        #globalvars.root.add_widget (globalvars.universe.primary.view)#())                
        #print globalvars.universe.primary.view.id
        #globalvars.universe.primary.view.update(clear=True)
        
        Clock.schedule_interval(globalvars.universe.update, 1./1.)        
        
        return root
        
        
        

if __name__ == '__main__':
    GameApp().run()
