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
from kivy.properties import ListProperty
from kivy.graphics import Line, Color, Rotate, PushMatrix, PopMatrix, Translate
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.metrics import Metrics
from kivy.uix.bubble import Bubble, BubbleButton


import numpy as np
from functools import partial


import shipimage
import util
import modules


kv = '''
<ShipScreen@Screen>:
    name: 'ark screen'    
    pos_hint: {'center_x': 0.5, 'center_y': .5}
           
    
    ScrollView:
        id: shipscroll
               
        pos_hint: {'center_x': .5, 'center_y': .5}
                                                                         
            
        FloatLayout:
            id: shiplayout  
            size: (800, 3520)
            size_hint: None, None 
            #Image:
 
<RoomImage@Image>:
    size: '40dp','40dp'
    size_hint: None, None     
    
    Image:
        id: roomicon
        size: '30dp','30dp'
        size_hint: None, None 
        mipmap: True
    
    Image:
        id: sizeimg
        size: '20dp','20dp'
        size_hint: None, None
                           
'''

Builder.load_string(kv)

def densFix(coords):
    return (np.array(coords) * Metrics.density).tolist()

kv='''
<ModuleBubble>:
    orientation: 'vertical'
    size_hint: (None, None)
    Label:
        id: module_info
        text: "Shouldn't see this"       
    BubbleButton:
        text: 'Power Off'  
        id: togglebtn  
        on_press: root.on_toggle()
        size_hint: 1, 0.5
    
<EmptyRoomBubble>:    
    orientation: 'vertical'
    size_hint: (None, None)
    Label:
        id: room_info
        text: "Shouldn't see this"  
    BubbleButton:
        text:'<select module>'
        id: dropdownbtn
        size_hint: 1, 0.5
        DropDown:
            id: dropdown 
         
    BubbleButton:
        text: 'Build!'  
        id: buildbtn  
        on_press: self.parent.parent.buildclick()
        size_hint: 1, 0.5
    
'''

Builder.load_string(kv)

class EmptyRoomBubble(Bubble):
    def __init__(self,**kwargs):
        Bubble.__init__(self,**kwargs)
        self.room = kwargs['room_entry']
        self.ship = kwargs['ship']
        
        txt = 'Space: '+str(self.room['size'])+'\n'
        txt += 'Power: '+str(self.room['power'])+'\n'
        txt += 'Avail. Tokens:'
        
        #print txt
        self.ids['room_info'].text = txt
        self.selection = None
        
        self.populate_dropdown()
        self.refresh()
        
    def populate_dropdown(self):
        
            
        self.ids['dropdownbtn'].bind(on_release=self.ids['dropdown'].open)
        self.ids['dropdown'].bind(on_select=lambda instance, x: setattr(self.ids['dropdownbtn'], 'text', x))  
        
        for i in modules.all_modules:
            v = modules.all_modules[i]
            if v['Size'] == self.room['size'] and v['Power'] <= self.room['power']:            
                btn = Button(text=v['Name'], font_size='12dp', size_hint_y=None, height='50dp')
                btn.entry = i
                btn.bind(on_release = lambda btn: self.select(btn.entry))#self.ids['dropdown'].select(btn.text))
                self.ids['dropdown'].add_widget(btn)          
        
    def select(self,entry):
        self.selection = entry
        v = modules.all_modules[entry]
        self.ids['dropdown'].select(v['Name'])        
        print "making class",entry
        
    def buildclick(self):
        if self.selection is not None:             
            room_class = util.class_for_name('modules',self.selection)
            self.room['module'] = room_class(ship = self.ship)
            print self.parent.parent.parent
            self.parent.parent.parent.refresh()
        self.suicide()
                
        
    def refresh(self,time=0):
        #self.ids['room_info'].text = self.module.txt_info() 
        #self.ids['togglebtn'].text = 'Power Off' if self.module.toggled else 'Power On'     
        
        self.ids['room_info'].texture_update()        
        
        self.size = self.ids['room_info'].texture_size
        self.width += 50
        self.height = '120dp'        
        
    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)       
        touch.pop()
        if not touched:
            self.suicide()
        return super(EmptyRoomBubble, self).on_touch_down(touch)           

    def suicide(self):
        if self.parent is not None: self.parent.remove_widget(self)    

class ModuleBubble(Bubble):    

    def __init__(self,**kwargs):
        Bubble.__init__(self,**kwargs)
        self.module = kwargs['module']
        #self.ids['asteroid_info'].text = self.ast.txt_info()
        #
        self.refresh()
        Clock.schedule_interval(self.refresh, 1)
        
    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)       
        touch.pop()
        if not touched:
            self.suicide()
        return super(ModuleBubble, self).on_touch_down(touch)   
        
    def on_toggle(self):
        self.module.on_toggle()
        self.module.update(0)
        
        self.refresh()
                

    def delete_clock(self, touch, *args):
        if 'event' in touch.ud: Clock.unschedule(touch.ud['event'])
                
    def refresh(self,time=0):
        self.ids['module_info'].text = self.module.txt_info() 
        self.ids['togglebtn'].text = 'Power Off' if self.module.toggled else 'Power On'     
        
        self.ids['module_info'].texture_update()        
        
        self.size = self.ids['module_info'].texture_size
        #print self.size
        self.width += 30
        self.height = '150dp'
        
    def suicide(self):
        if self.parent is not None: self.parent.remove_widget(self)        
        
    '''def on_harvest(self,*args):
        harv = globalvars.universe.ship.harvest(self.ast)
        if harv: self.parent.remove_widget(self)'''

class RoomImage(Image):
    def __init__(self, **kwargs):
        self.rentry = kwargs['room_entry']
        self.room = self.rentry['module']
        self.rsize = self.rentry['size']
        if self.room: 
            self.source = 'img/icon/modules/filled-generic.png'
        else:
            self.source = 'img/icon/modules/empty-generic.png'
        Image.__init__(self,**kwargs)
        
        
        #loc = self.room.img_dict['sizeloc'] if self.room else [0.5, 0.5]
        #self.ids['sizeimg'].pos_hint = loc 
        
        '''self.background_color = [0.3,0.3,0.3,1.0]
        if self.room:
            self.background_color = [0.8,0.8,0.8,1.0] #TODO room symbols
            if self.room.active:
                self.background_color = [0.2,1.0,0.2,1.0] #TODO edit of room symbol'''
                
        self.refresh()                
                
    def go_to_loc(self,loc):
        self.center = loc
        self.ids['sizeimg'].center = (np.array(loc)+np.array(self.sizeoffset)).tolist()
        self.ids['roomicon'].center = loc
        
    def refresh(self):
        self.room = self.rentry['module']
        self.rsize = self.rentry['size']

        if self.room: 
            self.source = 'img/icon/modules/filled-generic.png'
        else:
            self.source = 'img/icon/modules/empty-generic.png'
    
        self.ids['roomicon'].source = self.room.img_dict['icon'] if self.room else 'img/icon/modules/blank.png'
        self.ids['roomicon'].color = self.room.img_dict['icon color'] if self.room else [0.8,0.8,0.8,1]
        
        self.ids['roomicon'].texture_update() 
        
        self.ids['sizeimg'].source = ''.join(['img/icon/modules/',str(self.rsize),'.png'])
        if self.room and not self.room.img_dict['displaysize']: self.ids['sizeimg'].color = [1,1,1,0]
        self.ids['sizeimg'].texture_update() 
        
        self.sizeoffset = self.room.img_dict['sizeloc'] if self.room else [0, 0]
    
        self.color = self.room.color if self.room else [1,1,1,1]      
        self.texture_update() 
        
    def touched(self,tpos):
        bubble = ModuleBubble(module=self.room)
        bubble.pos = tpos
        
        self.parent.add_widget(bubble)                       

    def on_touch_down(self, touch):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        touched = self.collide_point(*touch.pos)
        touch.apply_transform_2d(self.to_window)
        tpos = touch.pos        
        touch.pop()
        if touched:
            if self.room:
                self.touched(tpos)
            else:
                bubble = EmptyRoomBubble(room_entry = self.rentry, ship = self.parent.parent.parent.ship)
                bubble.pos = tpos
                
                self.parent.add_widget(bubble)
                #TODO touched empty room!  Build menu maybe?
                
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(RoomImage, self).on_touch_down(touch) 

class ShipScreen(Screen):
    def __init__(self,**kwargs):
        super(ShipScreen,self).__init__(**kwargs)
        
        self.ship = kwargs['ship'] #TODO catch errors if missing
        #print shipimage.ship_dict,self.ship.shipclass,'prefix', '/ShipRoomsRotate.png'
        
        
        
        
    def on_pre_enter(self):
        interior_img = Image(source=shipimage.ship_dict[self.ship.shipclass]['prefix']+ '/ShipRooms.png',color=[0.5,0.5,0.5,1.], allow_stretch=True, size_hint= [None, None])
        interior_img.size = densFix(interior_img.texture.size)
        interior_img.pos_hint= {'center_x': .5, 'center_y': .5}
        self.ids['shiplayout'].add_widget(interior_img)
        self.ids['shiplayout'].size = (np.array(interior_img.size)+100).tolist()
        
        #add rooms
        for r in self.ship.rooms:
            #mimg = r['module'].module_image()
            rimg = RoomImage( room_entry=r )
            #butt.text = str(r['size'])
            #room_name = 'room'+str(r['size'])+'_'
            #room_name += 'empty.png' if not r['module'] else 'full.png'
            b_center = np.array(self.ids['shiplayout'].center)+np.array(r['loc'])*Metrics.density        
            #print r_center, np.array(self.ids['shiplayout'].center),np.array(r['loc'])       
            #room_img = Image(source='img/room/'+room_name, center = r_center.tolist(), size=[40,40], size_hint= [None, None])
            #rimg.center = b_center.tolist()
            rimg.go_to_loc(b_center.tolist())
            #rimg.ids['sizeimg'].pos_hint = 0.5,0.5
            self.ids['shiplayout'].add_widget(rimg)
            
        self.ids['shipscroll'].scroll_x = 0.5
        self.ids['shipscroll'].scroll_y = 0.5
        
        #add panels
        #add status
        
    def on_leave(self):  
        self.ids['shiplayout'].clear_widgets()         
        
    def refresh(self):
        self.quick_refresh()
        Clock.schedule_interval(self.quick_refresh, 0.25)
    
    def quick_refresh(self, *args):
        for c in self.ids['shiplayout'].children:
            if hasattr(c,'refresh'): c.refresh()
       
        
