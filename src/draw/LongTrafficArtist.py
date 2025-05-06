import cairo
import math
from LongTraffic import LongTraffic
from Artist import *

class LongTrafficArtist(Artist):

    def __init__(self):

        super().__init__()
        
        # Setup intersection
        self.road = LongTraffic()

        self._setup_context()


    def draw_road(self):

        # Upper curb
        self.ctx.rectangle(0, 0,
                           self.road.get_width(), 
                           self.road.sw)
        
        # Lowver curb
        self.ctx.rectangle(0, self.road.sw + self.road.nl * self.road.lw,
                           self.road.get_width(), 
                           self.road.sw)
        self.ctx.set_source_rgb(0.3, 0.3, 0.3)
        self.ctx.fill()

        self.ctx.rectangle(0, self.road.sw,
                           self.road.get_width(), 
                           self.road.nl * self.road.lw)
        self.ctx.set_source_rgb(0.7, 0.7, 0.7)
        self.ctx.fill()

        # Draw outer lines
        self.ctx.move_to(0.0, self.road.sw)
        self.ctx.line_to(self.road.get_width(), self.road.sw)

        self.ctx.move_to(0.0, self.road.get_height() - self.road.sw)
        self.ctx.line_to(self.road.get_width(), self.road.get_height() - self.road.sw)

        self.ctx.set_source_rgb(1.0,1.0,1.0)
        self.ctx.set_line_width(0.5)
        self.ctx.stroke()

        # Draw inner lines
        for i in range(self.road.nl):
            self.ctx.move_to(0, self.road.sw + i*self.road.lw)
            self.ctx.line_to(self.road.get_width(), self.road.sw + i*self.road.lw)

        self.ctx.set_dash([self.road.get_width()/10,
                           self.road.get_width()/10],
                           self.road.get_width()/20)
        self.ctx.set_source_rgb(1.0,1.0,1.0)
        self.ctx.set_line_width(0.5)
        self.ctx.stroke()

        # Unset the dash
        self.ctx.set_dash([])


    def draw_rel_vehicle(self, x, y, color, static=False, oncoming=False):
        p = self.road.get_rel_lane_pos(x, y , rel='c')
        if static:
            self.draw_static(p, 'e', color)
        elif oncoming:
            self.draw_vehicle(p, 'w', color)
        else:
            self.draw_vehicle(p, 'e', color)


    def draw_abs_vehicle(self, x, y, color, static=False):
        p = self.road.get_abs_lane_pos(x, y , rel='c')
        if not static:
            self.draw_vehicle(p, 'e', color)
        else:
            self.draw_static(p, 'e', color)


    def draw_lc(self, x, y, target, color, offset=1):
        p = self.road.get_rel_lane_pos(x, y , rel='f')
        self.ctx.move_to(p[0], p[1])

        # Initial control points
        xc = p[0] + self.D_CTRL
        yc = p[1]

        # Target point
        a = p[0] + self.road.cs - offset
        b = p[1] - target * self.road.lw
        
        # Target control points
        ac = a - self.D_CTRL
        bc = b

        self.ctx.curve_to(xc, yc, ac, bc, a, b)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((a+0.5, b), 'e', color)

    
    def draw_scaled_arrow(self, x, y, color, scaling=1.0, extension=-1):
        p = self.road.get_rel_lane_pos(x, y , rel='f')
        self.ctx.move_to(p[0], p[1])

        q = p[0] + self.road.cs* scaling + extension 
        self.ctx.line_to(q, p[1])
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((q+0.5, p[1]), 'e', color)


    def draw_reverse_arrow(self, x, y, color, scaling=1.0, extension=-1):
        p = self.road.get_rel_lane_pos(x, y , rel='r')
        self.ctx.move_to(p[0], p[1])

        q = p[0] - self.road.cs* scaling - extension 
        self.ctx.line_to(q, p[1])
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((q-0.5, p[1]), 'w', color)


    def draw_reverse_lc(self, x, y, target, color, offset=1):
        p = self.road.get_rel_lane_pos(x, y , rel='r')
        self.ctx.move_to(p[0], p[1])

        # Initial control points
        xc = p[0] - self.D_CTRL
        yc = p[1]

        # Target point
        a = p[0] - self.road.cs + offset
        b = p[1] - target * self.road.lw
        
        # Target control points
        ac = a + self.D_CTRL
        bc = b

        self.ctx.curve_to(xc, yc, ac, bc, a, b)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((a-0.5, b), 'w', color)


    def draw_aborted_lc(self, x, y, target, color, offset=1):
        p = self.road.get_rel_lane_pos(x, y , rel='f')
        self.ctx.move_to(p[0], p[1])

        # Initial control points
        xc = p[0] + self.D_CTRL/2
        yc = p[1]

        # Target point
        a = p[0] + (self.road.cs - offset) / 2
        b = p[1] - (target * self.road.lw) / 2
        
        # Target control points
        ac = a - self.D_CTRL/2
        bc = b

        self.ctx.curve_to(xc, yc, ac, bc, a, b)

        # Initial control points
        acc = a + self.D_CTRL/2
        bcc = b

        # Target point
        c = a + (self.road.cs - offset) / 2
        d = b + (target * self.road.lw) / 2
        
        # Target control points
        cc = c - self.D_CTRL/2
        dc = d

        self.ctx.curve_to(acc, bcc, cc, dc, c, d)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((c+0.5, d), 'e', color)


    def draw_approaching(self, x, y, color, offset=1):

        p = self.road.get_rel_lane_pos(x, y , rel='f')
        self.ctx.move_to(p[0], p[1])


        # Target point
        a = p[0] + self.road.cs - offset
        b = p[1]

        self.ctx.line_to(a, b)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((a+0.5, b), 'e', color)
        self.draw_arrowhead((a, b), 'e', color,)

    
    def draw_motorcycle(self, x, y, color, l_fac=0.75, w_fac=0.5):
        p = self.road.get_rel_lane_pos(x, y , rel='f')
        q = (p[0]-self.road.cw*l_fac, p[1])
        self.ctx.translate(q[0], q[1])
        self.ctx.save()
        self.ctx.scale(l_fac, w_fac)
        self.ctx.rectangle(-.5* self.road.cl, -.5* self.road.cw,self.road.cl,self.road.cw)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.fill()
        lw = 0.01
        self.draw_arrowhead((0.5 * self.road.cl,0), 0,
                            shade_of(color, 0.5), 
                            self.road.cw - lw,
                            self.road.cl/3 - 0.5*lw,
                            lw=lw, fill=True)
        self.ctx.restore()
        self.ctx.translate(-q[0], -q[1])

