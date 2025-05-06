import cairo
import math
from ComplexIntersection import ComplexIntersection
from Artist import *

class ComplexArtist(Artist):

    def __init__(self):

        super().__init__()

        # Setup intersection
        self.road = ComplexIntersection()
        self._setup_context()


    def draw_intersection(self):
        # Draw base
        self.ctx.rectangle(0, 0, self.road.get_width(), 
                                self.road.get_height())  # Rectangle(x0, y0, x1, y1)
        self.ctx.set_source_rgb(0.7, 0.7, 0.7)  # Solid color
        self.ctx.fill()

        # Draw the curb
        for i in range(4):
            c = self.road.get_sidewalk(i)
            self.ctx.rectangle(c[0], c[1], self.road.sw, self.road.sw)
            self.ctx.set_source_rgb(0.3, 0.3, 0.3)
            self.ctx.fill()

        W = self.road.get_width()
        H = self.road.get_height()

        # Draw the incoming lanes
        for l, r in zip([self.road.lanes['n'], self.road.lanes['e'], self.road.lanes['s'], self.road.lanes['w']],
                        [self.road.lanes['s'], self.road.lanes['w'], self.road.lanes['n'], self.road.lanes['e']]):

            self.ctx.set_line_width(0.5)
            self.ctx.set_source_rgb(1.0,1.0,1.0)

            for i in range(1,l):
                self.ctx.move_to(self.road.sw + i*self.road.lw, 0)
                self.ctx.line_to(self.road.sw + i*self.road.lw, self.road.sw)
            self.ctx.set_dash(self.ROAD_DASH,0.5)
            self.ctx.stroke()

            self.ctx.move_to(self.road.sw + l*self.road.lw, 0)
            self.ctx.line_to(self.road.sw + l*self.road.lw, self.road.sw)
            self.ctx.set_dash([])
            self.ctx.stroke()

            for i in range(1,r):
                self.ctx.move_to(self.road.sw + (l + i) * self.road.lw, 0)
                self.ctx.line_to(self.road.sw + (l + i) * self.road.lw, self.road.sw)
            self.ctx.set_dash(self.ROAD_DASH,0.5)
            self.ctx.stroke()

            self.ctx.translate(self.road.get_width()/2, self.road.get_height()/2)
            self.ctx.rotate(math.pi/2)
            self.ctx.translate(-self.road.get_width()/2, -self.road.get_height()/2)

            self.ctx.set_dash([])


    def draw_entering_vehicle(self, pos, color, l=0):
        """Draws a vehicle at the entry position of the intersection
            If offset is given, at the center of the entry.
            If offset == 'i' (--> inner), closest to the begin of the
            intersection area.
            If offset == 'o' (--> outer), as far away from the
            intersection areas as possible.
        """

        dir = mirror(pos)
        p = self.road.get_entry(pos, l)    
        self.draw_vehicle(p, dir, color)

    
    def draw_passing_vehicle(self, pos, color, offset=0, lat=0):

        dir = mirror(pos)
        h = dir2rad(dir)
        p = self.road.get_passing_pos(pos)
        q = trans_in_dir(dir, offset*self.road.lw, p)
        r = trans_in_dir(rot_cw(dir), lat*self.road.lw, q)
        self.draw_vehicle(r, dir, color)


    def draw_left_turn(self, pos, color,l=0):
        self.draw_entering(pos, l=l)
        # Draw the arc
        self.draw_lt(mirror(pos), self.road.get_lt_radius(l))
        
        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, rot_cw(pos), color)


    def draw_partial_left_turn(self, pos, color, partial, extension=0, l=0, dr=0):
        # Init
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()
        
        # Draw the dashed part of the arc
        r = self.road.get_lt_radius(l) + dr * self.road.lw
        h_middle = self.draw_lt(mirror(pos), r, end=partial)
        
        # Save the middle position
        p_middle = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        if partial > 0: self.ctx.set_dash(self.DASH)
        self.ctx.stroke()

        # Unset the dash
        self.ctx.set_dash([])

        # Draw the solid part of the art
        h_end = self.draw_lt(mirror(pos), r, x=p_start,  start=partial)

        self.line_in_dir(h_end, extension)
        p_end = self.ctx.get_current_point()
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(p_end, rot_cw(pos), color)

        return (p_middle, h_middle)
    

    def draw_incomplete_left_turn(self, pos, color, start=0, end=1, extension=0, l=0, invis=False, double=False):
        # Init
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()
        if start != 0:
            self.ctx.new_path()
        
        # Draw the dashed part of the arc
        h_middle = self.draw_lt(mirror(pos), self.road.get_lt_radius(l), x=p_start, start=start, end=end)
        
        # Save the middle position
        p_middle = self.ctx.get_current_point()

        if end == 1:
            self.line_in_dir(h_middle, extension)
        
        p_end = self.ctx.get_current_point()
        
        if invis:
            self.ctx.new_path()
        else:
            # Finalize the arc
            self.ctx.set_source_rgb(color[0], color[1], color[2])
            self.ctx.set_line_width(0.2)
            self.ctx.stroke()
            # Draw the arrowhead at the final position
            self.draw_arrowhead(p_end, h_middle, color)

            if double:
                p_double = trans_in_dir(h_middle, 0.6, p_end)
                self.draw_arrowhead(p_double, h_middle, color)

        return (p_middle, h_middle)
    

    def draw_partial_right_turn(self, pos, color, partial, extension=0, l=0, dr=0):
        # Init
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()
        
        # Draw the dashed part of the arc
        r = self.road.get_rt_radius(l) + dr*self.road.lw
        h_middle = self.draw_rt(mirror(pos),r, end=partial)
        
        # Save the middle position
        p_middle = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        if partial > 0: self.ctx.set_dash(self.DASH)
        self.ctx.stroke()

        # Unset the dash
        self.ctx.set_dash([])

        # Draw the solid part of the art
        h_end = self.draw_rt(mirror(pos), r, x=p_start,  start=partial)

        self.line_in_dir(h_end, extension)
        p_end = self.ctx.get_current_point()
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(p_end, rot_acw(pos), color)

        return (p_middle, h_middle)
    

    def draw_incomplete_right_turn(self, pos, color, start=0, end=1, extension=0, l=0, invis=False, double=False):
        # Init
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()
        if start != 0:
            self.ctx.new_path()
        
        # Draw the dashed part of the arc
        h_middle = self.draw_rt(mirror(pos), self.road.get_rt_radius(l), x=p_start, start=start, end=end)
        
        # Save the middle position
        p_middle = self.ctx.get_current_point()

        if end == 1:
            self.line_in_dir(h_middle, extension)
        
        p_end = self.ctx.get_current_point()
        
        if invis:
            self.ctx.new_path()
        else:
            # Finalize the arc
            self.ctx.set_source_rgb(color[0], color[1], color[2])
            self.ctx.set_line_width(0.2)
            self.ctx.stroke()
            # Draw the arrowhead at the final position
            self.draw_arrowhead(p_end, h_middle, color)

            if double:
                p_double = trans_in_dir(h_middle, 0.6, p_end)
                self.draw_arrowhead(p_double, h_middle, color)

        return (p_middle, h_middle)
    

    def draw_partial_u_turn(self, pos, color, partial, extension=0, l=0, dr=0):
        # Init
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()

        r = self.road.get_ut_radius(l) + dr*self.road.lw
        
        # Draw the dashed part of the arc
        self.road.get_ut_radius(l=l)
        h_middle = self.draw_ut(mirror(pos), r, end=partial)
        
        # Save the middle position
        p_middle = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        if partial > 0: self.ctx.set_dash(self.DASH)
        self.ctx.stroke()

        # Unset the dash
        self.ctx.set_dash([])

        # Draw the solid part of the art
        h_end = self.draw_ut(mirror(pos), r, x=p_start,  start=partial)

        self.line_in_dir(h_end, extension)
        p_end = self.ctx.get_current_point()
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(p_end, pos, color)

        return (p_middle, h_middle)
    

    def draw_incomplete_u_turn(self, pos, color, start=0, end=1, extension=0, l=0, invis=False, double=False):
        # Init
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()
        if start != 0:
            self.ctx.new_path()
        
        # Draw the dashed part of the arc
        h_middle = self.draw_ut(mirror(pos), self.road.get_ut_radius(l), x=p_start, start=start, end=end)
        
        # Save the middle position
        p_middle = self.ctx.get_current_point()

        if end == 1:
            self.line_in_dir(h_middle, extension)
        
        p_end = self.ctx.get_current_point()
        
        if invis:
            self.ctx.new_path()
        else:
            # Finalize the arc
            self.ctx.set_source_rgb(color[0], color[1], color[2])
            self.ctx.set_line_width(0.2)
            self.ctx.stroke()
            # Draw the arrowhead at the final position
            self.draw_arrowhead(p_end, h_middle, color)

            if double:
                p_double = trans_in_dir(h_middle, 0.6, p_end)
                self.draw_arrowhead(p_double, h_middle, color)

        return (p_middle, h_middle)
    

    def draw_partial_passing_straight(self, pos, color, partial, extension=0, l=0):
        self.draw_entering(pos, front=False, l=l)
        # Draw the line
        
        dist = self.road.get_pass_dist()
        
        self.line_in_dir(mirror(pos), dist * partial)

        # Save the middle position
        p_middle = self.ctx.get_current_point()
        
        # Finalize the line
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        if partial > 0: self.ctx.set_dash(self.DASH)
        self.ctx.stroke()

        # Unset the dash
        self.ctx.set_dash([])

        self.ctx.move_to(p_middle[0], p_middle[1])

        self.line_in_dir(mirror(pos), dist * (1-partial))
        self.line_in_dir(mirror(pos), extension)
        p_end = self.ctx.get_current_point()
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(p_end, mirror(pos), color)

        return (p_middle, mirror(pos))
    

    def draw_incomplete_passing_straight(self, pos, color, start=0, end=1, extension=0, l=0, invis=False, double=False):
        # Init
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()
        if start != 0:
            self.ctx.new_path()

        self.ctx.move_to(p_start[0], p_start[1])        
        self.move_in_dir(mirror(pos), self.road.get_pass_dist()*start)
        self.line_in_dir(mirror(pos), self.road.get_pass_dist()*(end - start))
        
        # Save the middle position
        p_middle = self.ctx.get_current_point()

        if end == 1:
            self.line_in_dir(mirror(pos), extension)
        
        p_end = self.ctx.get_current_point()
        
        if invis:
            self.ctx.new_path()
        else:
            # Finalize the arc
            self.ctx.set_source_rgb(color[0], color[1], color[2])
            self.ctx.set_line_width(0.2)
            self.ctx.stroke()
            # Draw the arrowhead at the final position
            self.draw_arrowhead(p_end, mirror(pos), color)

            if double:
                p_double = trans_in_dir(mirror(pos), 0.6, p_end)
                self.draw_arrowhead(p_double, mirror(pos), color)

        return (p_middle, dir2rad(mirror(pos)))

        
    def draw_right_turn(self, pos, color, l=0):
        self.draw_entering(pos, l=l)
        # Draw the arc
        h_new = self.draw_rt(mirror(pos), self.road.get_rt_radius(l))
        
        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, h_new, color)


    def draw_u_turn(self, pos, color, l=0):
        self.draw_entering(pos, l=l)
        # Draw the arc
        h_new = self.draw_ut(mirror(pos), self.road.get_ut_radius(l))
        
        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, h_new, color)


    def draw_passing_straight(self, pos, color, l=0):
        self.draw_entering(pos, l=l)
        # Draw the line
        self.line_in_dir(mirror(pos), self.road.get_pass_dist())

        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the line
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, mirror(pos), color)


    def draw_entering(self, pos, front=True, l=0):
        
        car_center = self.road.get_entry(pos,l)

        car_front = trans_in_dir(mirror(pos), self.road.cl/2, car_center)
        self.ctx.move_to(car_front[0], car_front[1])
        
        if front:
            p = car_front
            l = self.road.sw/2 - self.road.cl/2
        else: 
            p = car_center
            l = self.road.sw/2

        maneuver_start = trans_in_dir(mirror(pos), l, p)
        self.ctx.line_to(maneuver_start[0], maneuver_start[1])


    def draw_lane_change_passing_straight(self, color, lc_dist, l=0, dir=1, extension=3, enter=True):
        pos = 's'
        self.draw_entering(pos, front=False, l=l)
        p_start = self.ctx.get_current_point()
        if not enter:
            self.ctx.new_path()

        self.ctx.move_to(p_start[0], p_start[1])  
        
        
        lc_dist = lc_dist * self.road.lw

        # Draw the line
        dist = self.road.get_pass_dist()
        
        self.line_in_dir(mirror(pos), (dist - lc_dist)/2)

        D = 0.75*self.road.lw

        # Save the middle position
        p_lc_start = self.ctx.get_current_point()
        a = (p_lc_start[0], p_lc_start[1] - D)

        p_lc_end = (p_lc_start[0] - dir * self.road.lw, p_lc_start[1]-lc_dist)
        b = (p_lc_end[0], p_lc_end[1] + D) 

        self.ctx.curve_to(a[0], a[1], b[0], b[1], p_lc_end[0], p_lc_end[1])

        # Finalize the line
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)

        self.line_in_dir(mirror(pos), (dist - lc_dist)/2)
        self.line_in_dir(mirror(pos), extension)
        p_end = self.ctx.get_current_point()
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(p_end, mirror(pos), color)

        return (p_end, mirror(pos))


    
    def draw_entering_vru(self, pos, color): 
        p = self.road.get_VRU_pos(pos)
        self.draw_vru(p, color, width=self.road.ps)


    def draw_crossing_entering(self, pos, near, color):
        
        p = self.road.get_VRU_pos(pos)
        self.ctx.move_to(p[0], p[1])

        l = 2 * self.road.lw
        t = get_enter_target(pos, near, l)

        self.ctx.line_to(p[0]+t[0], p[1]+t[1])

        # Finalize the line
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead((p[0]+t[0], p[1]+t[1]), math.atan2(t[1], t[0]), color)


    def draw_crossing_exiting(self, pos, near, color):
        
        p = self.road.get_VRU_pos(pos)
        self.ctx.move_to(p[0], p[1])

        l = 2 * self.road.lw
        t = get_exit_target(pos, near, l)

        self.ctx.line_to(p[0]+t[0], p[1]+t[1])

        # Finalize the line
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead((p[0]+t[0], p[1]+t[1]), math.atan2(t[1], t[0]), color)


    def draw_entering_r_ex(self, pos, color):
            
        r = (self.road.sw - self.road.cl + self.road.lw) / 2.0
        p = self.road.get_VRU_pos(pos)

        # dir is the direction of the first move
        if pos == 'nw':
            dir = 's'
        elif pos == 'ne':
            dir = 'w'
        elif pos == 'se':
            dir = 'n'
        elif pos == 'sw':
            dir = 'e'

        self.ctx.move_to(p[0], p[1])
        h_new = self.draw_rt(dir, r)
       
        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, h_new, color)        


    def draw_entering_r_en(self, pos, color):
            
        r = (self.road.sw - self.road.cl + self.road.lw) / 2.0
        l = self.road.lw * 1.0

        p = self.road.get_VRU_pos(pos)

        # dir is the direction of the first move
        if pos == 'nw':
            dir = 'e'
        elif pos == 'ne':
            dir = 's'
        elif pos == 'se':
            dir = 'w'
        elif pos == 'sw':
            dir = 'n'

        self.ctx.move_to(p[0], p[1])
        h_new = self.draw_rt(dir, r)

        self.line_in_dir(h_new, l)
       
        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, h_new, color)


    def draw_entering_l_ex(self, pos, color):
            
        r = (self.road.sw - self.road.cl + self.road.lw) / 2.0
        l = self.road.lw * 1.0

        p = self.road.get_VRU_pos(pos)

        # dir is direction of the first move
        if pos == 'nw':
            dir='e'
        elif pos == 'ne':
            dir='s'
        elif pos == 'se':
            dir='w'
        elif pos == 'sw':
            dir='n'

        self.ctx.move_to(p[0], p[1])
        self.line_in_dir(dir, l)

        h_new = self.draw_lt(dir, r)
       
        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the arc
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, h_new, color)


    def draw_entering_l_en(self, pos, color):
            
        r = (self.road.sw - self.road.cl + self.road.lw) / 2.0
        l1 = self.road.lw * 1.0
        l2 = self.road.lw * 2.0

        p = self.road.get_VRU_pos(pos)

        # dir is direction of the first move
        if pos == 'nw':
            dir='s'
        elif pos == 'ne':
            dir='w'
        elif pos == 'se':
            dir='n'
        elif pos == 'sw':
            dir='e'

        self.ctx.move_to(p[0], p[1])
        self.line_in_dir(dir, l1)

        h = self.draw_lt(dir, r)

        c = self.line_in_dir(h, l2)

        # Save the final position
        e = self.ctx.get_current_point()
        
        # Finalize the line
        self.ctx.set_source_rgb(color[0], color[1], color[2])
        self.ctx.set_line_width(0.2)
        self.ctx.stroke()

        # Draw the arrowhead at the final position
        self.draw_arrowhead(e, h, color)
    
    