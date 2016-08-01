

market_size = 100

class MarketGrid(object):
    '''Handles the conversion from map coordinates to towns, divvying resources between townships to simulate a smoother map'''
    def __init__(self,size=(300,300)):
        self.grid = []
        self.size = [size[0]//market_size+1,size[1]//market_size+1]
        for x in range(self.size[0]):
            col=[]
            for y in range(self.size[1]):
                col.append(Market(index=(x,y)))
            self.grid.append(col)
            
    def local_markets(self,pos=(0,0)):
        '''returns a weighted list of markets relevant to a given point'''
        i_x = 1.*(pos[0] - pos[0]//market_size)/market_size
        i_y = 1.*(pos[1] - pos[1]//market_size)/market_size        
        x = pos[0]//market_size
        y = pos[1]//market_size
        
        dist_mult = [0, 0.25,1,0.25,0]
        
        _sum=0
        out=[]
        
        for x1 in range(-1,3):
            if x+x1 < 0 or x+x1 >= self.size[0]: continue
            xm = dist_mult[x1+1]*(1-i_x) + dist_mult[x1+2]*(i_x)
            for y1 in range(-1,3):
                if y+y1 < 0 or y+y1 >= self.size[1]: continue
                ym = dist_mult[y1+1]*(1-i_y) + dist_mult[y1+2]*(i_y)
                tm = xm*ym
                if tm:
                    _sum += tm     
                    out.append([self.grid[x+x1][y+y1], tm])
        for o in out:
            o[1] /= _sum
            
        return out                            
            

class Market(object):
    def __init__(self,index=(0,0)):
        self.index = index
        
        
        
        
if __name__ == "__main__":
    cg = MarketGrid(size=[200,500])        
    print cg.size
    print [i.index for i in cg.grid[0]]
    print 
    print cg.local_markets((0,0))
