import math
from Infra import *

class ComplexIntersection(Inftrastructure):

    def __init__(self, 
                 sidewalk_width=10):

        super().__init__()

        self.W_RAD = 0 * math.pi
        self.S_RAD = 0.5 * math.pi
        self.E_RAD = 1.0 * math.pi
        self.N_RAD = 1.5 * math.pi
        
        self.sw=sidewalk_width
        self.ps=(self.sw - self.cl)*0.75

        self.lanes = {'n': 2,  # Lanes incoming north
                      's': 2,  # Lanes incoming south
                      'w': 2,  # Lanes incoming west
                      'e': 2}  # Lanes incoming east


    def get_entry(self, d, l=0):
        if d=='s':
            pos = (self.get_width() - self.sw - (0.5 + l) * self.lw,
                   self.get_height() - 0.5 * self.sw)
        elif d=='w':
            pos = (0.5 * self.sw,
                   self.get_height() - self.sw - (0.5 + l) * self.lw)
        elif d=='n':
            pos = (self.sw + (0.5 + l) * self.lw,
                   0.5 * self.sw)
        elif d=='e':
            pos = (self.get_width() - 0.5 * self.sw,
                   self.get_height() - self.sw - (0.5 + l) * self.lw)
        else:
            return
        
        return pos
    

    def get_outer_entry(self, d, i_lane=0):

        if d=='s':
            pos = (self.sw + 1.5 * self.lw,
                    2.0 * self.sw + 2.0 * self.lw - 0.5 * self.cl)
        elif d=='w':
            pos = (0.5 * self.cl,
                    1.0 * self.sw + 1.5 * self.lw)
        elif d=='n':
            pos = (1 * self.sw + 0.5 * self.lw,
                    0.5 * self.cl)
        elif d=='e':
            pos = (2.0 * self.sw + 2 * self.lw - 0.5 * self.cl,
                    1 * self.sw + 0.5 * self.lw)
        else:
            return
        
        return pos
    

    def get_inner_entry(self, d):
        if d=='s':
            pos = (self.sw + 1.5 * self.lw,
                    1.0 * self.sw + 2.0 * self.lw + 0.5 * self.cl)
        elif d=='w':
            pos = (1.0 * self.sw - 0.5 * self.cl,
                    1.0 * self.sw + 1.5 * self.lw)
        elif d=='n':
            pos = (1 * self.sw + 0.5 * self.lw,
                   1.0 * self.sw - 0.5 * self.cl)
        elif d=='e':
            pos = (1.0 * self.sw + 2 * self.lw + 0.5 * self.cl,
                    1 * self.sw + 0.5 * self.lw)
        else:
            return
        
        return pos
    

    def get_maneuver_start(self, p):
        if p=='s':
            pos = (self.sw + 1.5 * self.lw,
                    1.0 * self.sw + 2 * self.lw)
        elif p=='w':
            pos = (1.0 * self.sw,
                    1.0 * self.sw + 1.5 * self.lw)
        elif p=='n':
            pos = (1.0 * self.sw + 0.5 * self.lw,
                    1.0 * self.sw)
        elif p=='e':
            pos = (1.0 * self.sw + 2 * self.lw,
                    1 * self.sw + 0.5 * self.lw)
        else:
            return
        
        return pos
    

    def get_passing_pos(self,p):
        if p=='s':
            pos = (self.sw + 1.5 * self.lw,
                    self.get_height() / 2)
        elif p=='w':
            pos = (self.get_width() / 2,
                    1.0 * self.sw + 1.5 * self.lw)
        elif p=='n':
            pos = (1.0 * self.sw + 0.5 * self.lw,
                    self.get_height() / 2)
        elif p=='e':
            pos = (self.get_width() / 2,
                    1 * self.sw + 0.5 * self.lw)
        else:
            return
        
        return pos
    
    
    def get_lt_radius(self, l=0):
        return (-0.5+self.lanes['s']+self.lanes['n']-l) * self.lw
    

    def get_rt_radius(self, l=0):
        return (0.5 + l) * self.lw
    

    def get_ut_radius(self, l=0):
        return (1.5 - l) * self.lw
    

    def get_pass_dist(self):
        return (self.lanes['w']+self.lanes['e']) * self.lw


    def get_sidewalk(self, n, tl=True):
        if n == 0:
            pos = (0, 0)
        elif n == 1:
            pos = (self.sw + (self.lanes['n'] + self.lanes['s']) * self.lw, 0)
        elif n == 2:
            pos = (self.sw + (self.lanes['n'] + self.lanes['s']) * self.lw, self.sw + (self.lanes['e'] + self.lanes['w']) * self.lw)
        elif n == 3:
            pos = (0, self.sw + (self.lanes['e'] + self.lanes['w']) * self.lw)
        else:
            return

        if not tl:
            pos = (pos[0] + 0.5 * self.sw, pos[1] + 0.5 * self.sw)

        return pos
    

    def get_VRU_pos(self, pos):

        if pos == 'nw':
            return (0.5 * (self.sw + self.cl),
                    0.5 * (self.sw + self.cl))
        elif pos == 'sw':
            return (0.5 * (self.sw + self.cl),
                    self.get_width() - 0.5 * (self.sw + self.cl))
        elif pos == 'se':
            return (self.get_width() - 0.5 * (self.sw + self.cl),
                    self.get_width() - 0.5 * (self.sw + self.cl))
        elif pos == 'ne':
            return (self.get_width() - 0.5 * (self.sw + self.cl),
                    0.5 * (self.sw + self.cl))
    
    
    def get_width(self):
        return 2 * self.sw + (self.lanes['n'] + self.lanes['s']) * self.lw


    def get_height(self):
        return 2 * self.sw + (self.lanes['e'] + self.lanes['w']) * self.lw
    

    def get_car_tl(self, dir, d):
        """"Get top left of a car (in image coordinates)"""
        if d=='n' or d=="s":
            return (dir[0] - 0.5 * self.cw,
                    dir[1] - 0.5 * self.cl)
        elif d=='e' or d=="w":
            return (dir[0] - 0.5 * self.cl, 
                    dir[1] - 0.5 * self.cw)
        else:
            return (0,0)


    def get_car_fc(self, pos, d):
        """"Get front of a car (relative to car)"""
        if d=='n':
            return (pos[0],
                    pos[1] - 0.5 * self.cl)
        elif d=='e':
            return (pos[0] - 0.5 * self.cl,
                    pos[1])
        elif d=='s':
            return (pos[0],
                    pos[1] + 0.5 * self.cl)
        elif d=='e':
            return (pos[0] + 0.5 * self.cl,
                    pos[1])
        else:
            return (0,0)







