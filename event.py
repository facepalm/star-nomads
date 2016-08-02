import util

class Event(object):
    def __init__(self):
        self.id = util.register(self)
        
        self.scan_strength = 1 
        self.current_scan = 0
        
            
        
