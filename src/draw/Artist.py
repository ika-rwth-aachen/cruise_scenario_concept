import cairo
import math
from Infra import *

class Artist():

    def __init__(self,
                 width=512,
                 c_ego=(0.0 ,0.0, 1.0), 
                 c_obj=(1.0 ,0.0, 0.0)):
    
        self.WIDTH = width

        self.C_EGO = c_ego
        self.C_OBJ = c_obj

        self.D_CTRL = 3.0
        self.DASH = [0.5, 0.5]

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 
                                          self.WIDTH, self.WIDTH)
        self.ctx = cairo.Context(self.surface)
        
        self.road = Inftrastructure()
        self.ROAD_DASH = [0.4 * self.road.cl, 0.4 * self.road.cl]#, 0.6*self.road.cl]


    def _setup_context(self):

        self.HEIGHT = int(self.WIDTH * self.road.get_height() / self.road.get_width())

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 
                                          self.WIDTH, self.HEIGHT)
        self.ctx = cairo.Context(self.surface)

        self.ctx.scale(self.WIDTH / self.road.get_width(),
                       self.HEIGHT / self.road.get_height())
        

    def set_road(self, road):
        self.road = road
        self._setup_context()


    def write(self, name):
        self.surface.write_to_png(name)
    

    def move_in_dir(self, h, l):
        x = self.ctx.get_current_point()
        a = trans_in_dir(h, l, x)
        self.ctx.move_to(a[0], a[1])

    
    def line_in_dir(self, h, l):
        x = self.ctx.get_current_point()
        a = trans_in_dir(h, l, x)
        self.ctx.line_to(a[0], a[1])

    
    def draw_vehicle(self, center, heading, color):
        # Translate to where we want to draw
        self.ctx.translate(center[0], center[1])
        # Rotate to align context with the desired heading
        h = dir2rad(heading)  # Working with angles
        self.ctx.rotate(h)

        # Draw what we wandt to draw
        # A simple rectangle
        self.ctx.rectangle(-.5* self.road.cl, -.5* self.road.cw,self.road.cl,self.road.cw)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.fill()


        lw = 0.01
        self.draw_arrowhead((0.5 * self.road.cl,0), 0,
                            shade_of(color, 0.5), 
                            self.road.cw - lw,
                            self.road.cl/3 - 0.5*lw,
                            lw=lw, fill=True)  # For testing
        
        # Rotate back
        self.ctx.rotate(-h)
        self.ctx.translate(-center[0], -center[1])


    def draw_vru(self, center, color, width=2):
        self.ctx.arc(center[0], center[1], width / 2.0, 0, 2*math.pi)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.fill()

    
    def draw_static(self, center, heading, color):
        # Translate to where we want to draw
        self.ctx.translate(center[0], center[1])
        # Rotate to align context with the desired heading
        h = dir2rad(heading)  # Working with angles
        self.ctx.rotate(h)

        # Draw what we wandt to draw
        # A simple rectangle
        self.ctx.rectangle(-.5* self.road.cl, -.5* self.road.cw,self.road.cl,self.road.cw)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.fill()


        self.ctx.move_to(-.5* self.road.cl, -.5* self.road.cw)
        self.ctx.line_to(.5* self.road.cl, .5* self.road.cw)

        self.ctx.move_to(-.5* self.road.cl, .5* self.road.cw)
        self.ctx.line_to(.5* self.road.cl, -.5* self.road.cw)

        shaded = shade_of(color, 0.5)
        self.ctx.set_source_rgb(shaded[0], shaded[1], shaded[2])
        self.ctx.stroke()

        # Rotate back
        self.ctx.rotate(-h)
        self.ctx.translate(-center[0], -center[1])

    
    def draw_arrowhead(self, pos, dir, color, w=0.5, h=0.5, lw=0.2, fill=False):
        
        if isinstance(dir, int) or isinstance(dir, float):
            # Translate to where we want to draw
            self.ctx.translate(pos[0], pos[1])
            # Rotate to align context with the desired heading
            self.ctx.rotate(dir)
            self.draw_arrowhead((0,0), 'e',
                                color, 
                                w=w,
                                h=h,
                                lw=lw, fill=fill)
            
            # Rotate back
            self.ctx.rotate(-dir)
            self.ctx.translate(-pos[0], -pos[1])
        
        else:
            self.ctx.move_to(pos[0], pos[1])

            if dir == 'n':
                self.ctx.line_to(pos[0] + w / 2.0, pos[1] + h)
                self.ctx.line_to(pos[0] - w / 2.0, pos[1] + h)
            elif dir == 'e':
                self.ctx.line_to(pos[0]-h, pos[1] - w / 2.0)
                self.ctx.line_to(pos[0]-h, pos[1] + w / 2.0)
            elif dir == 's':
                self.ctx.line_to(pos[0] + w / 2.0, pos[1] - h)
                self.ctx.line_to(pos[0] - w / 2.0, pos[1] - h)
            elif dir == 'w':
                self.ctx.line_to(pos[0] + h, pos[1] - w / 2.0)
                self.ctx.line_to(pos[0] + h, pos[1] + w / 2.0)

            #self.ctx.line_to(pos[0], pos[1])
            self.ctx.close_path()

            self.ctx.set_source_rgb(color[0], color[1], color[2])
            self.ctx.set_line_width(lw)
            
            if fill:
                self.ctx.fill()
            else:
                self.ctx.stroke()
        


    def draw_lt(self, h, r, x=None, start=0.0, end=1.0):
        """Uses context to draw a left turn of specified radius
        args:
            h:  starting angle of turn
            r:  radius of turn
            x:  starting position of turn, if not specified, taken from
                context
        """

        # If we get no starting position, get it from the drawing context
        if not x:
            x = self.ctx.get_current_point()

        # If we get a direction string, transform it to a number
        if isinstance(h, str):
            h = dir2rad(h)

        # Move to the center of the arc
        center = trans_in_dir(rot_acw(h), r, x)

        h0 = rot_cw(h)
        h1 = h
        dh = h1 - h0

        ha = h0 + start * dh
        hb = h0 + end * dh
        
        # Draw the arc
        self.ctx.arc_negative(center[0], center[1], r,
                              ha, 
                              hb)
        
        # Return the resulting angle
        return rot_acw(hb)
    

    def draw_rt(self, h, r, x=None, start=0.0, end=1.0):
        """Uses context to draw a left turn of specified radius
        args:
            h:  starting angle of turn
            r:  radius of turn
            x:  starting position of turn, if not specified, taken from
                context
        """

        # If we get no starting position, get it from the drawing context
        if not x:
            x = self.ctx.get_current_point()

        # If we get a direction string, transform it to a number
        if isinstance(h, str):
            h = dir2rad(h)

        # Move to the center of the arc
        center = trans_in_dir(rot_cw(h), r, x)

        h0 = rot_acw(h)
        h1 = h
        dh = h1 - h0

        ha = h0 + start * dh
        hb = h0 + end * dh
        
        # Draw the arc
        self.ctx.arc(center[0], center[1], r,
                     ha, 
                     hb)
        
        # Return the resulting angle
        return rot_cw(hb)
    

    def draw_ut(self, h, r, x=None, start=0.0, end=1.0):
        """Uses context to draw a left turn of specified radius
        args:
            h:  starting angle of turn
            r:  radius of turn
            x:  starting position of turn, if not specified, taken from
                context
        """

        # If we get no starting position, get it from the drawing context
        if not x:
            x = self.ctx.get_current_point()

        # If we get a direction string, transform it to a number
        if isinstance(h, str):
            h = dir2rad(h)

        # Move to the center of the arc
        center = trans_in_dir(rot_acw(h), r, x)

        h0 = rot_cw(h)
        h1 = rot_acw(h,1)
        dh = h1 - h0

        ha = h0 + start * dh
        hb = h0 + end * dh
        
        # Draw the arc
        self.ctx.arc_negative(center[0], center[1], r,
                              ha, 
                              hb)
        
        # Return the resulting angle
        return rot_acw(hb, 1)
    

def shade_of(color, factor):
    
    # If it is larger than 1, interpret it as percentage
    if abs(factor) > 1: factor / 100

    r, g, b = color

    if factor < 0:
        new_r = r * (1 + factor)
        new_g = g * (1 + factor)
        new_b = b * (1 + factor)
    else: 
        new_r = r + (1 - r) * factor
        new_g = g + (1 - g) * factor
        new_b = b + (1 - b) * factor

    return (new_r, new_g, new_b)


def dir2rad(d):
    if d=='e':
        return 0 * math.pi
    elif d=='s':
        return 0.5 * math.pi
    elif d=='w':
        return 1.0 * math.pi
    elif d=='n':
        return 1.5 * math.pi
    else:
        return d


def rad2dir(r):
    if is_direction(r):
        return r

    r = r % (2*math.pi)
    if math.isclose(r, 0.0 * math.pi):
        return 'e'
    elif math.isclose(r, 0.5 * math.pi):
        return 's'
    elif math.isclose(r, 1.0 * math.pi):
        return 'w'
    elif math.isclose(r, 1.5 * math.pi):
        return 'n'
    else:
        raise ValueError('Value does not match an angle')


def is_direction(a):
    if not isinstance(a, str):
        return False
    elif a in ['e', 's', 'w', 'n']:
        return True
    else:
        return False


def trans_in_dir(h, l, i=(0,0)):
    if isinstance(h, str):
        h = dir2rad(h)
    return (i[0] + math.cos(h)*l, i[1] + math.sin(h)*l)


def mirror(p):
    if type(p) == int or type(p) == float:
        return p + math.pi
    elif p == 'n':
        return 's'
    elif p == 'e':
        return 'w'
    elif p == 's':
        return 'n'
    elif p == 'w':
        return 'e'
    

def rot_cw(p, n=1.0):
    if type(p) == int or type(p) == float:
        return p + n*0.5*math.pi
    elif p == 'n':
        return 'e'
    elif p == 'e':
        return 's'
    elif p == 's':
        return 'w'
    elif p == 'w':
        return 'n'
    
    
def rot_acw(p, n=1.0):
    if type(p) == int or type(p) == float:
        return p - n*0.5*math.pi
    elif p == 'n':
        return 'w'
    elif p == 'w':
        return 's'
    elif p == 's':
        return 'e'
    elif p == 'e':
        return 'n'
    

def get_exit_init(d, near):

    if d == 'n':
        out = 'ne' if near else 'nw'
    elif d == 'e':
        out = 'se' if near else 'ne'
    elif d == 's':
        out = 'sw' if near else 'se'
    elif d == 'w':
        out = 'nw' if near else 'sw'
    else:
        raise ValueError("Not an applicable direction")

    return out


def get_exit_target(p, near, l):

    if p == 'ne':
        out = (-l, 0) if near else (0, l)
    elif p == 'se':
        out = (0, -l) if near else (-l, 0)
    elif p == 'sw':
        out = (l, 0) if near else (0, -l)
    elif p == 'nw':
        out = (0, l) if near else (l, 0)
    else:
        raise ValueError("Not an applicable position")

    return out


def get_enter_init(d, near):

    if d == 'n':
        out = 'nw' if near else 'ne'
    elif d == 'e':
        out = 'ne' if near else 'se'
    elif d == 's':
        out = 'se' if near else 'sw'
    elif d == 'w':
        out = 'sw' if near else 'nw'
    else:
        raise ValueError("Not an applicable direction")

    return out


def get_enter_target(p, near, l):

    if p == 'ne':
        out = (0, l) if near else (-l, 0)
    elif p == 'se':
        out = (-l, 0) if near else (0, -l) 
    elif p == 'sw':
        out = (0, -l) if near else (l, 0)
    elif p == 'nw':
        out = (l, 0) if near else (0, l)
    else:
        raise ValueError("Not an applicable position")

    return out
