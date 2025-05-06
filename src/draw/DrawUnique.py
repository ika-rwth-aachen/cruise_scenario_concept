from Artist import *
from EnterExitArtist import EnterExitArtist
from LongTrafficArtist import LongTrafficArtist
from LongTraffic import LongTraffic
from ComplexArtist import ComplexArtist
from JunctionArtist import IntersectionArtist
from SimpleIntersection import SimpleIntersection

def draw_approach_lat_leaving_ta_from_left():
    art = EnterExitArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=1))
    
    art.draw_road()

    art.draw_ego(art.C_EGO)
    art.draw_ego_arrow(art.C_EGO)

    art.draw_exiting_crossing_obj(True, art.C_OBJ)
    art.draw_exiting_crossing_turn(True, art.C_OBJ)

    art.write('img/' + 'approach_lat_leaving_traffic_area_from_left' +'.png')


def draw_approach_lat_leaving_ta_from_right():
    art = EnterExitArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=1, n_ego=1))
    
    art.draw_road()

    art.draw_ego(art.C_EGO)
    art.draw_ego_arrow(art.C_EGO)

    art.draw_exiting_crossing_obj(False, art.C_OBJ)
    art.draw_exiting_crossing_turn(False, art.C_OBJ)

    art.write('img/' + 'approach_lat_leaving_traffic_area_from_right' +'.png')


def draw_incomplete_enter_lead_l():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=3, n_pos=3, l_ego=1, n_ego=0))
    
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_lc(0,0,0,art.C_EGO)

    art.draw_rel_vehicle(1,1,(0.5 ,0.5, 0.5))
    art.draw_lc(1,1,-1,(0.5 ,0.5, 0.5))

    art.draw_rel_vehicle(2,1,art.C_OBJ)
    art.draw_lc(2,1,-1,art.C_OBJ)

    art.write('img/' + 'incomplete_enter_lead_l' +'.png')


def draw_incomplete_enter_lead_r():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=3, n_pos=3, l_ego=1, n_ego=0))
    
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_lc(0,0,0,art.C_EGO)

    art.draw_rel_vehicle(1,-1,(0.5 ,0.5, 0.5))
    art.draw_lc(1,-1,1,(0.5 ,0.5, 0.5))

    art.draw_rel_vehicle(2,-1,art.C_OBJ)
    art.draw_lc(2,-1,1,art.C_OBJ)

    art.write('img/' + 'incomplete_enter_lead_r' +'.png')
    

def draw_follow_TJ():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0, front_space=False))

    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0, art.C_EGO, scaling=0.25)

    art.draw_rel_vehicle(0.5,0,art.C_OBJ)
    art.draw_scaled_arrow(0.5,0, art.C_OBJ, scaling=0.25)
    art.draw_rel_vehicle(1.0,0,(.5,.5,.5))
    art.draw_scaled_arrow(1.0,0, (.5,.5,.5), scaling=0.25)
    art.draw_rel_vehicle(1.5,0,(.5,.5,.5))
    art.draw_scaled_arrow(1.5,0, (.5,.5,.5), scaling=0.25)
    art.draw_rel_vehicle(2,0,(.5,.5,.5))
    art.draw_scaled_arrow(2,0, (.5,.5,.5), scaling=0.25)

    art.write('img/' + 'follow_TJ' +'.png')


def draw_approach_TJ():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0, front_space=False))

    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_approaching(0,0,art.C_EGO)

    art.draw_rel_vehicle(1,0,art.C_OBJ)
    art.draw_scaled_arrow(1,0, art.C_OBJ, scaling=0.25)
    art.draw_rel_vehicle(1.5,0,(.5,.5,.5))
    art.draw_scaled_arrow(1.5,0, (.5,.5,.5), scaling=0.25)
    art.draw_rel_vehicle(2,0,(.5,.5,.5))
    art.draw_scaled_arrow(2,0, (.5,.5,.5), scaling=0.25)

    art.write('img/' + 'approach_TJ' +'.png')


def draw_approach_static():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=0))
    
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_approaching(0,0,art.C_EGO)

    art.draw_rel_vehicle(1,0,art.C_OBJ, static=True)

    art.write('img/' + 'approach_static' +'.png')


def draw_exit_u_turning():
    art = EnterExitArtist()
    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=0))
    art.draw_road()

    art.draw_ego(art.C_EGO)
    art.draw_ego_arrow(art.C_EGO)

    art.draw_leading_obj(art.C_OBJ)
    art.draw_u_turn(art.C_OBJ, oncoming=False)

    art.write('img/' + 'exit_u-turning' +'.png')


def draw_enter_u_turning():
    art = EnterExitArtist()
    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=0))
    art.draw_road()

    art.draw_ego(art.C_EGO)
    art.draw_ego_arrow(art.C_EGO)

    art.draw_oncoming_obj(art.C_OBJ)
    art.draw_u_turn(art.C_OBJ, oncoming=True)

    art.write('img/' + 'enter_u-turning' +'.png')    


def draw_standstill():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=0))
    
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)

    art.write('img/' + 'standstill' +'.png')


def draw_approach_reversing():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=0))
    
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_approaching(0,0,art.C_EGO)

    art.draw_rel_vehicle(1.25,0,art.C_OBJ)
    art.draw_reverse_arrow(1.25,0,art.C_OBJ, scaling=0.25)

    art.write('img/' + 'approach_reversing' +'.png')


def draw_approach_oncoming():
    art = LongTrafficArtist()

    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0, front_space=False))

    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_approaching(0,0,art.C_EGO)

    art.draw_rel_vehicle(2,0,art.C_OBJ, oncoming=True)
    art.draw_reverse_arrow(2,0,art.C_OBJ)

    art.write('img/' + 'approach_oncoming' +'.png')


def draw_rear_obj_approaching():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=1))
    
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0,art.C_EGO)

    art.draw_rel_vehicle(-1,0,art.C_OBJ)
    art.draw_approaching(-1,0,art.C_OBJ)

    art.write('img/' + 'rear_obj_approaching' +'.png')


def draw_close_obj_behind():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=1))
    
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0,art.C_EGO, scaling=0.5)

    art.draw_rel_vehicle(-0.5,0,art.C_OBJ)
    art.draw_scaled_arrow(-0.5,0,art.C_OBJ, scaling=0.5)

    art.write('img/' + 'close_obj_behind' +'.png')


def draw_enter_oncoming_within_ego_TA():
    art = LongTrafficArtist()

    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0, front_space=False))

    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0,art.C_EGO)

    art.draw_rel_vehicle(2,1,art.C_OBJ, oncoming=True)
    art.draw_reverse_lc(2,1,-1,art.C_OBJ)

    art.write('img/' + 'enter_oncoming_within_ego_traffic_area' +'.png')


def draw_enter_oncoming_entering_ego_TA():
    art = LongTrafficArtist()

    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0, front_space=False))

    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0,art.C_EGO)

    art.draw_rel_vehicle(2,-1,art.C_OBJ, oncoming=True)
    art.draw_reverse_lc(2,-1,1,art.C_OBJ)

    art.write('img/' + 'enter_oncoming_entering_ego_traffic_area' +'.png')


def draw_exit_oncoming_within_ego_TA():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0, front_space=False))

    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0,art.C_EGO)

    art.draw_rel_vehicle(2,0,art.C_OBJ, oncoming=True)
    art.draw_reverse_lc(2,0,1,art.C_OBJ)

    art.write('img/' + 'exit_oncoming_within_ego_traffic_area' +'.png')


def draw_exit_oncoming_leaving_ego_TA():
    art = LongTrafficArtist()
    
    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0, front_space=False))

    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0,art.C_EGO)

    art.draw_rel_vehicle(2,0,art.C_OBJ, oncoming=True)
    art.draw_reverse_lc(2,0,-1,art.C_OBJ)

    art.write('img/' + 'exit_oncoming_leaving_ego_traff_area' +'.png')


def draw_passed_in_lane_l():
    art = LongTrafficArtist()

    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=1, car_spacing=1, margin=4))
    art.draw_road()

    art.draw_rel_vehicle(0,-0.15,art.C_EGO)
    art.draw_scaled_arrow(0,-0.15,art.C_EGO, extension=0, scaling=0.7)

    art.draw_motorcycle(-1,0.28,art.C_OBJ)
    art.draw_scaled_arrow(-1,0.28, art.C_OBJ, extension=1, scaling=6)

    art.write('img/' + 'passed_in_lane_l' +'.png')


def draw_passed_in_lane_r():
    art = LongTrafficArtist()

    art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=1, car_spacing=1, margin=4))
    art.draw_road()

    art.draw_rel_vehicle(0,0.15,art.C_EGO)
    art.draw_scaled_arrow(0,0.15,art.C_EGO, extension=0, scaling=0.7)

    art.draw_motorcycle(-1,-0.28,art.C_OBJ)
    art.draw_scaled_arrow(-1,-0.28, art.C_OBJ, extension=1, scaling=6)

    art.write('img/' + 'passed_in_lane_r' +'.png')


def draw_approach_lat_entering_traffic_area_from_left():
    art = EnterExitArtist()
    art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=1, n_ego=1))
    art.draw_road()

    art.draw_ego(art.C_EGO)
    art.draw_ego_arrow(art.C_EGO)

    art.draw_entering_obj_turning(False, art.C_OBJ)
    art.draw_crossing_turn(False, True, art.C_OBJ)

    art.write('img/' + 'approach_lat_entering_traffic_area_from_left' +'.png')


def draw_close_obj_side_in_intersection_left():

    art = ComplexArtist()

    SHIFT_FAC = 0.4

    art.draw_intersection()

    art.draw_partial_left_turn('s', art.C_EGO, partial=1, l=0)
    art.draw_partial_right_turn('s', art.C_EGO, partial=1, l=0)
    art.draw_partial_u_turn('s', art.C_EGO, partial=1, l=0)
    (p_ego, h_ego) = art.draw_partial_passing_straight('s', art.C_EGO, partial=0.5, extension=1, l=0)
    art.draw_vehicle(p_ego, h_ego, art.C_EGO)

    # Shift the context
    art.ctx.translate(SHIFT_FAC * art.road.lw, 0)

    art.draw_partial_left_turn('s', art.C_OBJ, partial=1, l=1)
    art.draw_partial_right_turn('s', art.C_OBJ, partial=1, l=1)
    art.draw_partial_u_turn('s', art.C_OBJ, partial=1, l=1)
    (p_obj, h_obj) = art.draw_partial_passing_straight('s', art.C_OBJ, partial=0.5, extension=1, l=1)
    art.draw_vehicle(p_obj, h_obj, art.C_OBJ)

    # Shift the context back
    art.ctx.translate(-SHIFT_FAC * art.road.lw, 0)

    art.write('img/' + 'close_obj_side_in_intersection_left' + '.png')


def draw_close_obj_side_in_intersection_right():

    art = ComplexArtist()

    SHIFT_FAC = 0.4

    art.draw_intersection()

    art.draw_partial_left_turn('s', art.C_EGO, partial=1, l=1)
    art.draw_partial_right_turn('s', art.C_EGO, partial=1, l=1)
    art.draw_partial_u_turn('s', art.C_EGO, partial=1, l=1)
    (p_ego, h_ego) = art.draw_partial_passing_straight('s', art.C_EGO, partial=0.5, extension=1, l=1)
    art.draw_vehicle(p_ego, h_ego, art.C_EGO)

    # Shift the context
    art.ctx.translate(-SHIFT_FAC * art.road.lw, 0)

    art.draw_partial_left_turn('s', art.C_OBJ, partial=1, l=0)
    art.draw_partial_right_turn('s', art.C_OBJ, partial=1, l=0)
    art.draw_partial_u_turn('s', art.C_OBJ, partial=1, l=0)
    (p_obj, h_obj) = art.draw_partial_passing_straight('s', art.C_OBJ, partial=0.5, extension=1, l=0)
    art.draw_vehicle(p_obj, h_obj, art.C_OBJ)

    # Shift the context back
    art.ctx.translate(SHIFT_FAC * art.road.lw, 0)

    art.write('img/' + 'close_obj_side_in_intersection_right' + '.png')


def draw_intersection_lc_l():

    art = ComplexArtist()

    art.draw_intersection()
    art.draw_entering_vehicle('s', art.C_EGO, l=0)

    art.draw_lane_change_passing_straight(art.C_EGO, 3, l=0, dir=1)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=0, dr=-1)
    art.draw_partial_right_turn('s', art.C_EGO, 1, l=0, dr=1)
    art.draw_partial_u_turn('s', art.C_EGO, 1, l=0, dr=-0.5)

    art.write('img/' + 'intersection_lc_l' + '.png')


def draw_intersection_lc_r():

    art = ComplexArtist()

    art.draw_intersection()
    art.draw_entering_vehicle('s', art.C_EGO, l=1)

    art.draw_lane_change_passing_straight(art.C_EGO, 3, l=1, dir=-1)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=1, dr=1)
    art.draw_partial_right_turn('s', art.C_EGO, 1, l=1, dr=-1)
    art.draw_partial_u_turn('s', art.C_EGO, 1, l=1, dr=0.5)

    art.write('img/' + 'intersection_lc_r' + '.png')


def draw_intersection_enter_lead_l():

    art = ComplexArtist()

    art.draw_intersection()

    art.draw_entering_vehicle('s', art.C_EGO, l=0)

    art.draw_entering_vehicle('s', art.C_EGO, l=0)
    art.draw_partial_passing_straight('s', art.C_EGO, partial=0, l=0)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=0)
    art.draw_partial_right_turn('s', art.C_EGO, 1, l=0)
    art.draw_partial_u_turn('s', art.C_EGO, 1, l=0)

    art.draw_entering_vehicle('s', art.C_OBJ, l=1)

    art.draw_lane_change_passing_straight(art.C_OBJ, 3, l=1, dir=-1)
    art.draw_partial_left_turn('s', art.C_OBJ, 1, l=1, dr=1)
    art.draw_partial_right_turn('s', art.C_OBJ, 1, l=1, dr=-1)
    art.draw_partial_u_turn('s', art.C_OBJ, 1, l=1, dr=0.5)

    art.write('img/' + 'intersection_enter_lead_l' + '.png')
    


def draw_intersection_enter_lead_r():

    art = ComplexArtist()

    art.draw_intersection()

    art.draw_entering_vehicle('s', art.C_EGO, l=1)
    art.draw_partial_passing_straight('s', art.C_EGO, partial=0, l=1)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=1)
    art.draw_partial_right_turn('s', art.C_EGO, 1, l=1)
    art.draw_partial_u_turn('s', art.C_EGO, 1, l=1)

    art.draw_entering_vehicle('s', art.C_OBJ, l=0)

    art.draw_lane_change_passing_straight(art.C_OBJ, 3, l=0, dir=1)
    art.draw_partial_left_turn('s', art.C_OBJ, 1, l=0, dr=-1)
    art.draw_partial_right_turn('s', art.C_OBJ, 1, l=0, dr=1)
    art.draw_partial_u_turn('s', art.C_OBJ, 1, l=0, dr=-0.5)

    art.write('img/' + 'intersection_enter_lead_r' + '.png')


def draw_intersection_exit_lead_l():

    art = ComplexArtist()

    art.draw_intersection()

    art.draw_entering_vehicle('s', art.C_EGO, l=0)

    art.draw_partial_passing_straight('s', art.C_EGO, partial=0, l=0)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=0)
    art.draw_partial_right_turn('s', art.C_EGO, 1, l=0)
    art.draw_partial_u_turn('s', art.C_EGO, 1, l=0)

    art.draw_lane_change_passing_straight(art.C_OBJ, 3, l=0, dir=1, enter=False)
    art.draw_partial_left_turn('s', art.C_OBJ, 1, l=0, dr=-1)
    art.draw_partial_right_turn('s', art.C_OBJ, 1, l=0, dr=1)
    art.draw_partial_u_turn('s', art.C_OBJ, 1, l=0, dr=-0.5)

    (p_obj, h_obj) = art.draw_incomplete_passing_straight('s', art.C_OBJ, end=0.1, invis=True)
    art.draw_vehicle(p_obj, h_obj, art.C_OBJ)

    art.write('img/' + 'intersection_exit_lead_l' + '.png')
    


def draw_intersection_exit_lead_r():

    art = ComplexArtist()

    art.draw_intersection()

    art.draw_entering_vehicle('s', art.C_EGO, l=1)

    art.draw_partial_passing_straight('s', art.C_EGO, partial=0, l=1)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=1)
    art.draw_partial_right_turn('s', art.C_EGO, 1, l=1)
    art.draw_partial_u_turn('s', art.C_EGO, 1, l=1)

    art.draw_lane_change_passing_straight(art.C_OBJ, 3, l=1, dir=-1, enter=False)
    art.draw_partial_left_turn('s', art.C_OBJ, 1, l=1, dr=1)
    art.draw_partial_right_turn('s', art.C_OBJ, 1, l=1, dr=-1)
    art.draw_partial_u_turn('s', art.C_OBJ, 1, l=1, dr=0.5)

    (p_obj, h_obj) = art.draw_incomplete_passing_straight('s', art.C_OBJ, end=0.1, invis=True, l=1)
    art.draw_vehicle(p_obj, h_obj, art.C_OBJ)

    art.write('img/' + 'intersection_exit_lead_r' + '.png')


def draw_diverging_lead_within_ego_TA_r():

    art = ComplexArtist()

    art.draw_intersection()

    p_ego = art.road.get_entry('s')

    art.draw_partial_passing_straight('s', art.C_EGO, partial=1, l=1, extension=3)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=1, extension=3)
    art.draw_partial_u_turn('s', art.C_EGO, 1, l=1)

    art.ctx.translate(-0.5,0.5)

    (p_obj, h_obj) = art.draw_partial_right_turn('s', art.C_OBJ, 0.5, l=1, extension=3)
    art.draw_partial_passing_straight('s', art.C_OBJ, 1, l=1)
    art.draw_partial_left_turn('s', art.C_OBJ, 1, l=1)

    art.draw_vehicle(p_obj, h_obj, art.C_OBJ)
    art.ctx.translate(0.5,-0.5)

    art.draw_entering_vehicle('s', art.C_EGO, l=1)

    art.write('img/' + 'diverging_lead_within_ego_TA_r' + '.png')


def draw_reverse_approach_lat_r():

    art = EnterExitArtist()
    art.set_road(LongTraffic(n_pos=2, l_ego=0, n_lanes=2, n_ego=1, front_space=False))
    art._setup_context()

    art.draw_road()
    art.draw_ego(art.C_EGO)
    art.draw_ego_arrow(art.C_EGO, reverse=True)

    art.draw_entering_vru(True, art.C_EGO, reverse=True)
    art.draw_crossing(True, art.C_OBJ, reverse=True)

    art.write('img/' + 'reverse_approach_lat_r' + '.png')


def draw_reverse_approach_lat_l():

    art = EnterExitArtist()
    art.set_road(LongTraffic(n_pos=2, l_ego=0, n_lanes=2, n_ego=1, front_space=False))
    art._setup_context()

    art.draw_road()
    art.draw_ego(art.C_EGO)
    art.draw_ego_arrow(art.C_EGO, reverse=True)

    art.draw_entering_vru(False, art.C_EGO, reverse=True)
    art.draw_crossing(False, art.C_OBJ, reverse=True)

    art.write('img/' + 'reverse_approach_lat_l' + '.png')


def draw_diverging_lead_within_ego_TA_l():

    art = ComplexArtist()

    art.draw_intersection()

    p_ego = art.road.get_entry('s')

    art.draw_partial_passing_straight('s', art.C_EGO, partial=0, l=1, extension=3)
    art.draw_partial_right_turn('s', art.C_EGO, 1, l=1, extension=3)
    art.draw_partial_left_turn('s', art.C_EGO, 1, l=1)

    art.ctx.translate(-0.5,0.5)

    (p_obj, h_obj) = art.draw_partial_left_turn('s', art.C_OBJ, 0.5, l=1, extension=3)
    art.draw_partial_passing_straight('s', art.C_OBJ, 1, l=1)
    art.draw_partial_u_turn('s', art.C_OBJ, 1, l=1)
    art.draw_vehicle(p_obj, h_obj, art.C_OBJ)
    art.ctx.translate(0.5,-0.5)

    art.draw_entering_vehicle('s', art.C_EGO, l=1)

    art.write('img/' + 'diverging_lead_within_ego_TA_l' + '.png')


def draw_passing_oncoming():
    art = LongTrafficArtist()
    art.set_road(LongTraffic(n_pos=3, l_ego=0, n_lanes=2, n_ego=1, front_space=False))
    art._setup_context()

    art.draw_road()
    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_scaled_arrow(0,0,art.C_EGO)

    art.draw_rel_vehicle(0,1,art.C_OBJ,oncoming=True)
    art.draw_reverse_arrow(0,1,art.C_OBJ)

    art.write('img/' + 'passing_oncoming' + '.png')


def draw_passing_oncoming_in_intersection():
    art = IntersectionArtist()
    art.draw_intersection()

    (p_ego, h_ego) = art.draw_partial_passing_straight('s', art.C_EGO, 0.5, extension=2)
    (p_obj, h_obj) = art.draw_partial_passing_straight('n', art.C_OBJ, 0.5, extension=2)

    art.draw_partial_right_turn('s', art.C_EGO, 1, extension=2)
    art.draw_partial_left_turn('s', art.C_EGO, 1, extension=2)

    art.draw_partial_right_turn('w', art.C_OBJ, 1, extension=2)
    art.draw_partial_left_turn('e', art.C_OBJ, 1, extension=2)

    art.draw_vehicle(p_ego,h_ego,art.C_EGO)
    art.draw_vehicle(p_obj,h_obj,art.C_OBJ)

    art.write('img/' + 'passing_oncoming_in_intersection' + '.png')


def draw_multi_lcs_l():
    art = LongTrafficArtist()
    art.set_road(LongTraffic(l_ego=0))
    art._setup_context()
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_lc(0,0,2,art.C_EGO)

    art.write('img/' + 'multi_lcs_l' + '.png')
    

def draw_multi_lcs_r():
    art = LongTrafficArtist()
    art.set_road(LongTraffic(l_ego=2))
    art._setup_context()
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_lc(0,0,-2,art.C_EGO)

    art.write('img/' + 'multi_lcs_r' + '.png')


def draw_standstill():
    art = LongTrafficArtist()
    art.set_road(LongTraffic(n_lanes=3, l_ego=1, n_pos=3, n_ego=1, front_space=False))
    art.draw_road()
    art.draw_rel_vehicle(0,0,art.C_EGO, static=True)

    art.write('img/' + 'standstill' + '.png')


def draw_approach_overlapping_oncoming():
    art = LongTrafficArtist()
    art.set_road(LongTraffic(n_lanes=2, l_ego=0, n_pos=3, n_ego=0, front_space=False))
    art._setup_context()
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_approaching(0,0,art.C_EGO)
    art.draw_rel_vehicle(2,0.5,art.C_OBJ, oncoming=True)
    art.draw_reverse_arrow(2,0.5,art.C_OBJ)

    art.write('img/' + 'approach_overlapping_oncoming' + '.png')


def draw_diverging_lead_leaving_TA_after_node_r():

    art = IntersectionArtist()
    art.draw_intersection()

    (p_obj, h_obj) = art.draw_partial_passing_straight('s', art.C_OBJ, 0.7, arrow=False)
    art.draw_diverge_from_TA_after_node_r('n', art.C_OBJ)
    art.draw_vru(p_obj, art.C_OBJ, width=1.2)

    art.draw_partial_right_turn('s', art.C_OBJ, 1, arrow=False)
    art.draw_diverge_from_TA_after_node_r('e', art.C_OBJ, dash=True)

    art.draw_partial_left_turn('s', art.C_OBJ, 1, arrow=False)
    art.draw_diverge_from_TA_after_node_r('w', art.C_OBJ, dash=True)

    art.draw_incomplete_passing_straight('s', art.C_EGO, end=0.4)
    art.draw_partial_right_turn('s', art.C_EGO, 1)
    art.draw_partial_left_turn('s', art.C_EGO, 1)
    art.draw_entering_vehicle('s', art.C_EGO)

    art.write('img/' + 'diverging_lead_leaving_TA_after_node_r' + '.png')


def draw_diverging_lead_leaving_TA_after_node_l():

    art = IntersectionArtist()
    art.draw_intersection()

    (p_obj, h_obj) = art.draw_partial_passing_straight('s', art.C_OBJ, 0.7, arrow=False)
    art.draw_diverge_from_TA_after_node_l('n', art.C_OBJ)
    art.draw_vru(p_obj, art.C_OBJ, width=1.2)

    art.draw_partial_right_turn('s', art.C_OBJ, 1, arrow=False)
    art.draw_diverge_from_TA_after_node_l('e', art.C_OBJ, dash=True)

    art.draw_partial_left_turn('s', art.C_OBJ, 1, arrow=False)
    art.draw_diverge_from_TA_after_node_l('w', art.C_OBJ, dash=True)

    art.draw_incomplete_passing_straight('s', art.C_EGO, end=0.4)
    art.draw_partial_right_turn('s', art.C_EGO, 1)
    art.draw_partial_left_turn('s', art.C_EGO, 1)
    art.draw_entering_vehicle('s', art.C_EGO)

    art.write('img/' + 'diverging_lead_leaving_TA_after_node_l' + '.png')

def draw_diverging_lead_leaving_TA_before_node_r():

    art = IntersectionArtist()
    art.set_road(SimpleIntersection(sidewalk_width=8))
    art._setup_context()
    art.draw_intersection()

    art.draw_incomplete_passing_straight('s', art.C_EGO, end=0.7)
    art.draw_partial_right_turn('s', art.C_EGO, 1)
    art.draw_partial_left_turn('s', art.C_EGO, 1)
    art.draw_entering_vehicle('s', art.C_EGO, offset='o')

    p = art.draw_diverge_from_TA_before_node_r('s', art.C_OBJ)
    art.draw_vru(p, art.C_OBJ, width=1.2)

    art.write('img/' + 'diverging_lead_leaving_TA_before_node_r' + '.png')


def draw_diverging_lead_leaving_TA_before_node_l():

    art = IntersectionArtist()
    art.set_road(SimpleIntersection(sidewalk_width=8))
    art._setup_context()
    art.draw_intersection()

    art.draw_incomplete_passing_straight('s', art.C_EGO, end=0.7)
    art.draw_partial_right_turn('s', art.C_EGO, 1)
    art.draw_partial_left_turn('s', art.C_EGO, 1)
    art.draw_entering_vehicle('s', art.C_EGO, offset='o')

    p = art.draw_diverge_from_TA_before_node_l('s', art.C_OBJ)
    art.draw_vru(p, art.C_OBJ, width=1.2)

    art.write('img/' + 'diverging_lead_leaving_TA_before_node_l' + '.png')


def draw_unique(c):

    art = None

    if c.get_name(c) == 'approach_lat_leaving_traffic_area_from_left':
        draw_approach_lat_leaving_ta_from_left()
    elif c.get_name(c) == 'approach_lat_leaving_traffic_area_from_right':
        draw_approach_lat_leaving_ta_from_right()
    elif c.get_name(c) == 'incomplete_enter_lead_l':
        draw_incomplete_enter_lead_l()
    elif c.get_name(c) == 'incomplete_enter_lead_r':
        draw_incomplete_enter_lead_r()
    elif c.get_name(c) == 'approach_static':
        draw_approach_static()
    elif c.get_name(c) == 'exit_u-turning':
        draw_exit_u_turning()
    elif c.get_name(c) == 'enter_u-turning':
        draw_enter_u_turning()
    elif c.get_name(c) == 'follow_TJ':
        draw_follow_TJ()
    elif c.get_name(c) == 'approach_TJ':
        draw_approach_TJ()
    elif c.get_name(c) == 'approach_reversing':
        draw_approach_reversing()
    elif c.get_name(c) == 'approach_oncoming':
        draw_approach_oncoming()
    elif c.get_name(c) == 'rear_obj_approaching':
        draw_rear_obj_approaching()
    elif c.get_name(c) == 'close_obj_behind':
        draw_close_obj_behind()
    elif c.get_name(c) == 'enter_oncoming_within_ego_traffic_area':
        draw_enter_oncoming_within_ego_TA()
    elif c.get_name(c) == 'enter_oncoming_entering_ego_traffic_area':
        draw_enter_oncoming_entering_ego_TA()
    elif c.get_name(c) == 'exit_oncoming_within_ego_traffic_area':
        draw_exit_oncoming_within_ego_TA()
    elif c.get_name(c) == 'exit_oncoming_leaving_ego_traffic_area':
        draw_exit_oncoming_leaving_ego_TA()
    elif c.get_name(c) == 'passed_in_lane_l':
        draw_passed_in_lane_l()
    elif c.get_name(c) == 'passed_in_lane_r':
        draw_passed_in_lane_r()
    elif c.get_name(c) == 'approach_lat_entering_traffic_area_from_left':
        draw_approach_lat_entering_traffic_area_from_left()
    elif c.get_name(c) == 'close_obj_side_in_intersection_right':
        draw_close_obj_side_in_intersection_right()
    elif c.get_name(c) == 'close_obj_side_in_intersection_left':
        draw_close_obj_side_in_intersection_left()
    elif c.get_name(c) == 'intersection_lc_l':
        draw_intersection_lc_l()
    elif c.get_name(c) == 'intersection_lc_r':
        draw_intersection_lc_r()
    elif c.get_name(c) == 'intersection_enter_lead_l':
        draw_intersection_enter_lead_l()
    elif c.get_name(c) == 'intersection_enter_lead_r':
        draw_intersection_enter_lead_r()
    elif c.get_name(c) == 'intersection_exit_lead_l':
        draw_intersection_exit_lead_l()
    elif c.get_name(c) == 'intersection_exit_lead_r':
        draw_intersection_exit_lead_r()
    elif c.get_name(c) == 'diverging_lead_within_ego_TA_l':
        draw_diverging_lead_within_ego_TA_l()
    elif c.get_name(c) == 'diverging_lead_within_ego_TA_r':
        draw_diverging_lead_within_ego_TA_r()
    elif c.get_name(c) == 'reverse_approach_lat_l':
        draw_reverse_approach_lat_l()
    elif c.get_name(c) == 'reverse_approach_lat_r':
        draw_reverse_approach_lat_r()
    elif c.get_name(c) == 'passing_oncoming':
        draw_passing_oncoming()
    elif c.get_name(c) == 'passing_oncoming_in_intersection':
        draw_passing_oncoming_in_intersection()
    elif c.get_name(c) == 'multi_lcs_r':
        draw_multi_lcs_r()
    elif c.get_name(c) == 'multi_lcs_l':
        draw_multi_lcs_l()
    elif c.get_name(c) == 'standstill':
        draw_standstill()
    elif c.get_name(c) == 'approach_overlapping_oncoming':
        draw_approach_overlapping_oncoming()
    elif c.get_name(c) == 'diverging_lead_leaving_TA_after_node_r':
        draw_diverging_lead_leaving_TA_after_node_r()
    elif c.get_name(c) == 'diverging_lead_leaving_TA_after_node_l':
        draw_diverging_lead_leaving_TA_after_node_l()
    elif c.get_name(c) == 'diverging_lead_leaving_TA_before_node_r':
        draw_diverging_lead_leaving_TA_before_node_r()
    elif c.get_name(c) == 'diverging_lead_leaving_TA_before_node_l':
        draw_diverging_lead_leaving_TA_before_node_l()
    else:
       print(c.get_name(c) + " not implemented.")
        
