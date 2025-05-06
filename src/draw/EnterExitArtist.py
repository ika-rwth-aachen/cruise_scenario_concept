import cairo
import math
from LongTraffic import LongTraffic
from Artist import *

class EnterExitArtist(Artist):

    def __init__(self,
                 width=256,
                 c_ego=(0.0 ,0.0, 1.0), 
                 c_obj=(1.0 ,0.0, 0.0)):
        
        super().__init__()
        
        # Setup intersection
        self.road = LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=1)

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


    def draw_ego(self, color):
        p = self.road.get_ego_pos('c')
        self.draw_vehicle(p, 'e', color)


    def draw_ego_arrow(self, color, l=6, reverse=False):
        k = 'f' if not reverse else 'r'
        p = self.road.get_ego_pos(k)
        self.ctx.move_to(p[0], p[1])
        dir = 'e' if not reverse else 'w'
        self.line_in_dir(dir, l)
        e = self.ctx.get_current_point()
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, dir, color)


    def draw_entering_obj_turning(self, near, color, reverse=False):
        p = self.road.get_enter_pos_turning(near, 'c')
        if (near and not reverse) or (not near and reverse):
            direction = 'n'
        else:
            direction = 's'
        self.draw_vehicle(p, direction, color)


    def draw_entering_obj_parallel(self, near, color):
        p = self.road.get_enter_pos_parallel(near, 'c')
        self.draw_vehicle(p, 'e', color)


    def draw_exiting_crossing_obj(self, left, color):
        y = 1 if left else -1
        p = self.road.get_rel_lane_pos(0, y, rel='c')
        self.draw_vehicle(p, 'e', color)

    
    def draw_exiting_leading_obj(self, color):
        p = self.road.get_exiting_pos('c')
        self.draw_vehicle(p, 'e', color)


    def draw_leading_obj(self, color):
        p = self.road.get_rel_lane_pos(1, 0, rel='c')
        self.draw_vehicle(p, 'e', color)


    def draw_oncoming_obj(self, color):
        p = self.road.get_rel_lane_pos(1, 1, rel='c')
        self.draw_vehicle(p, 'w', color)


    def draw_exiting_crossing_turn(self, left, color):
        y = 1 if left else -1
        p = self.road.get_rel_lane_pos(0, y, rel='f')

        self.ctx.move_to(p[0], p[1])
        if left:
            r = self.road.get_farside_entering_radius()
            h = self.draw_rt('e', r)
        else:
            r = self.road.get_nearside_entering_radius()
            h = self.draw_lt('e', r)

        # Save the final position
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, h, color)


    def draw_u_turn(self, color, oncoming=False):
        
        if oncoming:
            p = self.road.get_rel_lane_pos(1,1,'r')
            h = 'w'
        else:
            p = self.road.get_rel_lane_pos(1,0,'f')
            h = 'e'

        h_new = self.draw_ut(h, self.road.lw/2, p)
        
        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, h_new, color)


    def draw_entering_lc_forward(self, near, color, l=6):
        p = self.road.get_enter_pos_parallel(near, 'f')
        self.ctx.move_to(p[0], p[1])

        # Initial control points
        xc = p[0] + self.D_CTRL
        yc = p[1]

        # Target point
        a = p[0] + l
        if near:
            b = p[1] - self.road.lw
        else:
            b = p[1] + 2 * self.road.lw
        
        # Target control points
        ac = a - self.D_CTRL
        bc = b

        self.ctx.curve_to(xc, yc, ac, bc, a, b)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((a+0.5, b), 'e', color)


    def draw_entering_lc_reversing(self, near, color, l=5):
        p = self.road.get_enter_pos_parallel(near, 'r')
        self.ctx.move_to(p[0], p[1])

        # Initial control points
        xc = p[0] - self.D_CTRL
        yc = p[1]

        # Target point
        a = p[0] - l
        if near:
            b = p[1] - self.road.lw
        else:
            b = p[1] + 2 * self.road.lw
        
        # Target control points
        ac = a + self.D_CTRL
        bc = b

        self.ctx.curve_to(xc, yc, ac, bc, a, b)
        
        # Save the final position
        self.line_in_dir('e', l*2)
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, 'e', color)


    def draw_entering_turn(self, near, color):

        if near:
            p = self.road.get_enter_pos_turning(near, 'f')
            self.ctx.move_to(p[0], p[1])
            r = self.road.get_nearside_entering_radius()
            h = self.draw_rt('n', r)
        else:
            p = self.road.get_enter_pos_turning(near, 'r')
            self.ctx.move_to(p[0], p[1])
            r = self.road.get_farside_entering_radius()
            h = self.draw_lt('s', r)

        # Save the final position
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, h, color)

    def draw_crossing_turn(self, near, left, color):
        if near:
            p = self.road.get_enter_pos_turning(near, 'f')
            self.ctx.move_to(p[0], p[1])
            h = 'n'
        else:
            p = self.road.get_enter_pos_turning(near, 'r')
            self.ctx.move_to(p[0], p[1])
            h = 's'

        r = self.road.get_crossing_radius()

        if left:
            h = self.draw_lt(h, r)
        else:
            h = self.draw_rt(h, r)

        # Save the final position
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, h, color)


    def draw_entering_reversing_turn(self, near, color):

        if near:
            p = self.road.get_enter_pos_turning(near, 'f')
            self.ctx.move_to(p[0], p[1])
            r = self.road.get_nearside_entering_radius()
            h = self.draw_lt('n', r,)
        else:
            p = self.road.get_enter_pos_turning(near, 'r')
            self.ctx.move_to(p[0], p[1])
            r = self.road.get_farside_entering_radius()
            h = self.draw_rt('s', r,)

        # Save the final position
        self.line_in_dir('e', r)
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, 'e', color)


    def draw_exiting_lc_forward(self, near, color, l=5):
        p = self.road.get_exiting_pos('f')
        self.ctx.move_to(p[0], p[1])

        # Initial control points
        xc = p[0] + self.D_CTRL
        yc = p[1]

        # Target point
        a = p[0] + l
        if near:
            b = p[1] + self.road.lw
        else:
            b = p[1] - 2 * self.road.lw
        
        # Target control points
        ac = a - self.D_CTRL
        bc = b

        self.ctx.curve_to(xc, yc, ac, bc, a, b)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((a+0.5, b), 'e', color)


    def draw_exiting_lc_reversing(self, near, color, l=5):
        p = self.road.get_exiting_pos('f')
        self.ctx.move_to(p[0], p[1])

        self.line_in_dir('e', l)

        q = self.ctx.get_current_point()

        # Initial control points
        xc = q[0] - self.D_CTRL
        yc = q[1]

        # Target point
        a = q[0] - l
        if near:
            b = q[1] + self.road.lw
        else:
            b = q[1] - 2 * self.road.lw
        
        # Target control points
        ac = a + self.D_CTRL
        bc = b

        self.ctx.curve_to(xc, yc, ac, bc, a, b)
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead((a-0.5, b), 'w', color)


    def draw_exiting_turn_forward(self, near, color):
        p = self.road.get_exiting_pos('f')
        self.ctx.move_to(p[0], p[1])

        if near:
            r = self.road.get_nearside_entering_radius()
            h = self.draw_rt('e', r,)
        else:
            r = self.road.get_farside_entering_radius()
            h = self.draw_lt('e', r,)

        # Save the final position
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, h, color)
    
    
    def draw_exiting_turn_reversing(self, near, color):
        p = self.road.get_exiting_pos('f')
        self.ctx.move_to(p[0], p[1])

        if near:
            r = self.road.get_nearside_entering_radius()
            self.line_in_dir('e', r)
            h = self.draw_lt('w', r,)
        else:
            r = self.road.get_farside_entering_radius()
            self.line_in_dir('e', r)
            h = self.draw_rt('w', r)

        # Save the final position
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, h, color)


    def draw_entering_vru(self, near, color, width=2, reverse=False):
        p = self.road.get_enter_pos_turning(near, 'c', reverse=reverse)
        self.draw_vru(p, color, width=2)

    
    def draw_crossing(self, near, color, reverse=False):
        p = self.road.get_enter_pos_turning(near, 'c', reverse=reverse)
        self.draw_vru(p, color)
        self.ctx.move_to(p[0], p[1])
        l = 2*self.road.lw + 0.5*self.road.cw
        if near:
            l = -l
            h = 'n'
        else:
            h = 's'

        self.ctx.line_to(p[0], p[1]+l)

        # Save the final position
        e = self.ctx.get_current_point()

        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        self.draw_arrowhead(e, h, color)




