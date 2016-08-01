
import gps

class Ark(object):
    def __init__(self):
        self.style = 'Default' #Warship Worldship Junkship
        
    def location(self):
        return gps.get_location()        
