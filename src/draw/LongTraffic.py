import math
from Infra import *


class LongTraffic(Inftrastructure):

    def __init__(self,
                 n_lanes=3,
                 n_pos=3,
                 n_ego=1,
                 l_ego=1,
                 car_spacing=8,
                 margin=2,
                 sidewalk_width=5,
                 front_space=True):
        
        super().__init__()
        
        self.nl=n_lanes                 # Number of lanes
        self.np=n_pos                   # Number of positions in longitudinal direction
        self.ne=n_ego                   # Long position of the ego vehicle
        self.le=l_ego                   # Lane of the ego-vehicle
        self.cs=car_spacing             # Car spacing
        self.mar=margin                 # Margin at front and back of image
        self.sw=sidewalk_width
        self._front_space=front_space   # If true space is left before rightmost position


    def get_rel_lane_pos(self, x=0, y=0, rel='c'):

        # Sanitize input
        if x < self.max_pre():
            print("Requested x position to small.")
        if x > self.max_post(): # So we can move forward a bit
            print("Requested x position to large.")
        if y < self.max_right():
            print("Requested y position to small.")
        if y > self.max_left():
            print("Requested y position to large.")

        x_pos = self.mar \
                + (self.ne + x + 0.5) * self.cl \
                + (self.ne + x) * self.cs

        y_pos = (self.nl - self.le - y - 0.5) * self.lw + self.sw

        if rel == 'r':
            x_pos -= 0.5 * self.cl
        elif rel == 'f':
            x_pos += 0.5 * self.cl
        elif rel == 'tl':
            x_pos -= 0.5 * self.cl
            y_pos -= 0.5 * self.cw
        elif rel != 'c':
            raise ValueError('Position not of type f, c, or r.')

        return (x_pos, y_pos)
    

    def get_abs_lane_pos(self, x=0, y=0, rel='c'):

        # Sanitize input
        if x < 0:
            raise ValueError("Requested x position to small.")
        if x > self.np:
            raise ValueError("Requested x position to large.")
        if y < 0:
            raise ValueError("Requested y position to small.")
        if y > self.nl:
            raise ValueError("Requested y position to large.")

        x_pos = self.mar \
                + (x + 0.5) * self.cl \
                + x * self.cs

        y_pos = (self.nl - y - 0.5) * self.lw + self.sw

        if rel == 'r':
            x_pos -= 0.5 * self.cl
        elif rel == 'f':
            x_pos += 0.5 * self.cl
        elif rel == 'tl':
            x_pos -= 0.5 * self.cl
            y_pos -= 0.5 * self.cw
        elif rel != 'c':
            raise ValueError('Position not of type f, c, or r.')

        return (x_pos, y_pos)


    def max_pre(self):
        return -self.ne


    def max_post(self):
        return self.np - self.ne - 1


    def max_left(self):
        return self.nl - self.le - 1
        

    def max_right(self):
        return -self.le
    

    def get_enter_pos_turning(self, near=True, type='c', reverse=False):
        
        x  = self.mar \
             + (self.ne + 1.5) * self.cl \
             + (self.ne + 0.5) * self.cs
        
        if reverse:
            x = self.get_width() - x
            if not self._front_space: x = x + self.cs 
        
        if near:
            y = self.sw + (self.nl + 0.5) * self.lw
        else:
            y = self.sw - 0.5 * self.lw

        if type=='tl':
            x = x - self.cw / 2
            y = y - self.cl / 2
        elif type=='f':
            y = y - self.cl / 2
        elif type=='r':
            y = y + self.cl / 2
        elif type=='c':
            pass
        else:
            raise AttributeError("Incorrect type of position specification")
        
        return (x,y)
    

    def get_enter_pos_parallel(self, near=True, type='c'):
        x  = self.mar \
             + (self.ne + 1.5) * self.cl \
             + (self.ne + 0.5) * self.cs
        
        if near:
            y = self.sw + (self.nl + 0.5) * self.lw
        else:
            y = self.sw - 0.5 * self.lw

        if type=='tl':
            x = x - self.cl / 2
            y = y - self.cw / 2
        elif type=='f':
            x = x + self.cl / 2
        elif type=='r':
            x = x - self.cl / 2
        elif type=='c':
            pass
        else:
            raise AttributeError("Incorrect type of position specification")
        
        return (x,y)
    

    def get_ego_pos(self, rel='c'):
        return self.get_rel_lane_pos(0, 0, rel)
    

    def get_exiting_pos(self, rel='c'):
        return self.get_rel_lane_pos(1, 0, rel)
    

    def get_nearside_entering_radius(self):
        return (0.5 + self.le)* self.lw
    

    def get_farside_entering_radius(self):
        return (-0.5 + self.nl - self.le)* self.lw
    
    
    def get_crossing_radius(self):
        return 1.5 * self.lw
    

    def get_width(self):
        n_spacing = self.np if self._front_space else self.np - 1
        return self.mar * 2 \
               + self.np * self.cl \
               + (n_spacing) * self.cs


    def get_height(self):
        return self.nl * self.lw + 2 * self.sw
    