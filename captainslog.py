import time

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

kv = '''
<LogScreen@Screen>:
    name: 'log screen'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
    
    FloatLayout:
        Label:
            text:'Time'
            size_hint: 0.20 , 0.05
            pos_hint: { 'x':0.05, 'top': 0.95 }
        Label:
            text:'Message'
            size_hint: 0.60 , 0.05
            pos_hint: { 'x':0.30, 'top': 0.95 }
        
    
        ScrollView:
            id: resscroll               
            pos_hint: {'x': 0.05, 'y': 0.05}      
            size_hint: 0.9, 0.85
        
            StackLayout:
                id: msglist
                size_hint: 1.0,None            
                size: root.width, root.height
                pos_hint: {'center_x': 0.5, 'center_y': .5}
                padding: 20
                spacing: 10
                orientation: 'lr-tb'
                #height: 50
                
               
                
<SizedLabel>:
    text_size: root.width, None
    size: self.texture_size                
                
                
'''

Builder.load_string(kv)

class SizedLabel(Label):
    pass

class LogScreen(Screen):
    def __init__(self,**kwargs):
        Screen.__init__(self,**kwargs)
        self.log = kwargs['log']
        
        self.status_display = None
        self.display_limit = 100
        self.visible = False
        
    def on_pre_enter(self):
        self.visible = True
        self.refresh()          
                
    def on_leave(self):  
        self.visible = False    
        
    def refresh(self):
        if self.status_display: self.status_display.text = self.log.archive[-1]['Message']        
        
        if self.visible:
            msgs = self.ids['msglist']
            msgs.clear_widgets()
            num_msg = min(self.display_limit,len(self.log.archive))
            #tst = SizedLabel(text='check')
            #print tst.size
            #print Window.width
            #msgs.width = Window.width
            #msgs.height = num_msg*40
            for i in range(num_msg):
                txt = Button(text=str(self.log.archive[i]['Time']),size_hint=[None,None], size = [0.1*Window.width,50])
                txt.text_size = txt.size
                msgs.add_widget(txt)    
                msg = Button(text=self.log.archive[i]['Message'],size_hint=[None,None], size = [0.6*Window.width,50])
                msg.text_size = msg.size
                msgs.add_widget(msg)
        

class CaptainsLog(object):
    def __init__(self):
        self.archive = []
        self.screen=LogScreen(log=self)
        self.add('Log Initialized...',self)                
        
    def __getstate__(self):
        odict = self.__dict__.copy() # copy the dict since we change it
        del odict['screen']              # remove gui entry
        return odict
    
    def __setstate__(self,state):
        self.__dict__.update(state)   # update attributes
        self.screen=LogScreen(log=self)
        
    def add(self,message=None,obj=None,priority='LOW'):
        msg_time = time.time()
        self.archive.append({'Time':msg_time,'Source':obj,'Priority':priority,'Message':message})
        
        self.screen.refresh()
        
    def final_message(self):
        return self.archive[-1]        
        
