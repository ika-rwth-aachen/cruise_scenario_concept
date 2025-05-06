import owlready2 as owl
from JunctionArtist import IntersectionArtist
import JunctionArtist
from LongTrafficArtist import LongTrafficArtist
from EnterExitArtist import EnterExitArtist
from ComplexArtist import ComplexArtist
from DrawUnique import *


def main():

    global crs, sce, con
    global base_scenarios, superclasses, concepts, relations
    global drawn, concept_names

    # Load the ontology
    cruise_path = "cruise.owl"
    crs = owl.get_ontology(cruise_path)
    crs.load()

    # Get toplevel, scenario, and concept namespaces
    cns = "http://www.semanticweb.org/ika/vvmethods/cruise"
    sce = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/sce#")
    con = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/con#")

    # Extract what we are interested in
    base_scenarios = [c for c in crs.classes() if c.namespace == sce and not list(c.subclasses())]
    superclasses = [c for c in crs.classes() if c.namespace == sce and list(c.subclasses())]
    concepts = [c for c in crs.classes() if c.namespace == con]
    relations = list(crs.object_properties())

    concept_names = [c.name for c in concepts]

    #### Structuring the scenario space ####
    drawn = []

    # Draw what we can draw by interpreting concepts
    draw_intersection_conflicts()

    draw_intersection_ta_change()

    draw_long_transitions()

    draw_long_traffic_states()

    draw_neighboring_overlays()

    draw_approach_lat()

    draw_exit_leaving_ego_TA()

    draw_overlap_lane()

    draw_lane_change_with_oncoming()

    draw_non_parallel_intersection_overlays()

    draw_parallel_entry()

    draw_parallel_overlays()

    draw_intersection_states()

    draw_intersection_standstill()

    draw_reversing()

    draw_rear_obj_transitions()

    draw_neighbor_transitions()

    # Draw the unique stuff
    remaining = list(set(base_scenarios).difference(set(drawn)))
    for c in remaining:
        draw_unique(c)

def draw_intersection_conflicts():

    conflicts = [bs for bs in base_scenarios
                 if sce.intersection_conflict in bs.ancestors()
                 and not sce.conflict_with_TA_change in bs.ancestors()
                 and not sce.conflict_with_parallel_entry in bs.ancestors()]

    for c in conflicts:
        cons = get_concepts(c)

        print(c)
        print(cons)

        ia = IntersectionArtist()
        ia.draw_intersection()

        ia.draw_entering_vehicle('s', ia.C_EGO, offset='c')

        # Ego-maneuver 
        if applies_for_ego('passing_straight', cons):
             ia.draw_passing_straight('s', ia.C_EGO)
        elif applies_for_ego('right_turn', cons):
            ia.draw_right_turn('s', ia.C_EGO)
        elif applies_for_ego('left_turn', cons):
            ia.draw_left_turn('s', ia.C_EGO)
        elif applies_for_ego('u-turn', cons):
            ia.draw_u_turn('s', ia.C_EGO)
        else:
            raise AttributeError('No concept for ego-maneuver')

        # Obj-position
        if applies_for_obj('at_right', cons):
            op = 'e'
        elif applies_for_obj('at_left', cons):
            op = 'w'
        elif applies_for_obj('in_front_of', cons):
            op = 'n'
        else:
            raise AttributeError('No concept for object position')
        
        ia.draw_entering_vehicle(op, ia.C_OBJ, offset='')

        # Obj-maneuver
        if applies_for_obj('passing_straight', cons):
            ia.draw_passing_straight(op, ia.C_OBJ)
        elif applies_for_obj('right_turn', cons):
            ia.draw_right_turn(op, ia.C_OBJ)
        elif applies_for_obj('left_turn', cons):
            ia.draw_left_turn(op, ia.C_OBJ)
        elif applies_for_obj('u-turn', cons):
            ia.draw_u_turn(op, ia.C_OBJ)
        else:
            raise AttributeError('No concept for obj-maneuver')

        ia.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_intersection_ta_change():

    conflicts = [bs for bs in base_scenarios
                 if sce.conflict_with_TA_change in bs.ancestors()]

    for c in conflicts:
        cons = get_concepts(c)

        print(c)
        print(cons)

        ia = IntersectionArtist()
        ia.draw_intersection()

        ia.draw_entering_vehicle('s', ia.C_EGO, offset='o')

        # Ego-maneuver 
        if applies_for_ego('passing_straight', cons):
            ia.draw_passing_straight('s', ia.C_EGO, offset='o')
            p_exit_ego = 'n'
        elif applies_for_ego('right_turn', cons):
            ia.draw_right_turn('s', ia.C_EGO, offset='o')
            p_exit_ego = 'e'
        elif applies_for_ego('left_turn', cons):
            ia.draw_left_turn('s', ia.C_EGO, offset='o')
            p_exit_ego = 'w'
        elif applies_for_ego('u-turn', cons):
            ia.draw_u_turn('s', ia.C_EGO, offset='o')
            p_exit_ego = 's'
        else:
            raise AttributeError('No concept for ego-maneuver')

        # Object position
        # Object crossing
        if applies_for_obj('cross_ego_traffic_area', cons):
            if applies('before_node', cons):
                if applies_for_obj('at_right', cons):
                    p_obj = JunctionArtist.get_enter_init('s', True)
                    ia.draw_crossing_entering(p_obj, True, ia.C_OBJ)
                elif applies_for_obj('at_left', cons):
                    p_obj = JunctionArtist.get_enter_init('s', False)
                    ia.draw_crossing_entering(p_obj, False, ia.C_OBJ)
                else:
                    raise AttributeError('No concept for position before node')
            elif applies('behind_node', cons):
                if applies_for_obj('at_right', cons):
                    p_obj = JunctionArtist.get_exit_init(p_exit_ego, True)
                    ia.draw_crossing_exiting(p_obj, True, ia.C_OBJ)
                elif applies_for_obj('at_left', cons):
                    p_obj = JunctionArtist.get_exit_init(p_exit_ego, False)
                    ia.draw_crossing_exiting(p_obj, False, ia.C_OBJ)
                else:
                    raise AttributeError('No concept for position after node')        
            else:
                raise AttributeError('No concept for relation to node')
            
            ia.draw_entering_vru(p_obj, ia.C_OBJ)

        # Object entering
        elif applies_for_obj('enter_ego_traffic_area', cons):
            if applies('before_node', cons):
                if applies_for_obj('at_right', cons):
                    p_obj = JunctionArtist.get_enter_init('s', True)
                    ia.draw_entering_r_en(p_obj, ia.C_OBJ)
                elif applies_for_obj('at_left', cons):
                    p_obj = JunctionArtist.get_enter_init('s', False)
                    ia.draw_entering_l_en(p_obj, ia.C_OBJ)
                else:
                    raise AttributeError('No concept for position before node')
            elif applies('behind_node', cons):
                if applies_for_obj('at_right', cons):
                    p_obj = JunctionArtist.get_exit_init(p_exit_ego, True)
                    ia.draw_entering_r_ex(p_obj, ia.C_OBJ)
                elif applies_for_obj('at_left', cons):
                    p_obj = JunctionArtist.get_exit_init(p_exit_ego, False)
                    ia.draw_entering_l_ex(p_obj, ia.C_OBJ)
                else:
                    raise AttributeError('No concept for position after node')        
            else:
                raise AttributeError('No concept for relation to node')
            
            ia.draw_entering_vru(p_obj, ia.C_OBJ)

        else:
            raise AttributeError('Nor crossing nor entering')


        ia.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_merging_lcs(c, cons):

    if applies_for_ego('to_left', cons):
        l_ego = 0
        l_obj = 2
        d_ego = 1
    elif applies_for_ego('to_right', cons):
        l_ego = 2
        l_obj = -2
        d_ego = -1
    else:
        raise AttributeError('Got no direction for lane change.')

    art = LongTrafficArtist()
    art.set_road(LongTraffic(l_ego=l_ego))
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_lc(0,0,d_ego,art.C_EGO)

    art.draw_rel_vehicle(1,l_obj,art.C_OBJ)
    art.draw_lc(1,l_obj,-d_ego,art.C_OBJ)

    if applies_for_obj('behind', cons):
        art.draw_rel_vehicle(-1,d_ego,art.C_OBJ)
        art.draw_lc(-1,d_ego,0, art.C_OBJ)

    art.write('img/' + c.get_name(c) +'.png')
    drawn.append(c)
    

def draw_merging_cut_through(c, cons):

    if applies_for_ego('to_left', cons):
        l_obj = -1
        d_ego = 1
    elif applies_for_ego('to_right', cons):
        l_obj = 1
        d_ego = -1
    else:
        raise AttributeError('Got no direction for lane change.')

    art = LongTrafficArtist()
    art.set_road(LongTraffic())
    art.draw_road()

    art.draw_rel_vehicle(0,0,art.C_EGO)
    art.draw_lc(0,0,d_ego,art.C_EGO)

    art.draw_rel_vehicle(1,l_obj,art.C_OBJ)
    art.draw_lc(1,l_obj,2*d_ego, art.C_OBJ)

    if applies_for_obj('behind', cons):
        art.draw_rel_vehicle(-1,d_ego,art.C_OBJ)
        art.draw_lc(-1,d_ego,0, art.C_OBJ)

    art.write('img/' + c.get_name(c) +'.png')
    drawn.append(c)

        
def draw_long_transitions():
    long_transitions = [bs for bs in base_scenarios if sce.long_traffic_transition in bs.ancestors()]

    for c in long_transitions:

        cons = get_concepts(c)

        print(c)
        print(cons)

        # Catch the ones that need to be drawn separately
        if applies('incomplete', cons)\
        or c.get_name(c) == "multi_lcs_r"\
        or c.get_name(c) == "multi_lcs_l"\
        or c.get_name(c) == "enter_u-turning"\
        or c.get_name(c) == "exit_u-turning":
            continue
        
        if sce.merging_lcs in c.ancestors():
            if sce.cut_through in c.ancestors():
                draw_merging_cut_through(c, cons)
            else:
                draw_merging_lcs(c, cons)
        
        if applies_for_obj('enter_ego_traffic_area', cons)\
            or applies_for_obj('leaving_ego_traffic_area', cons):
            draw_entering_exiting(c, cons)

        
        if applies_for_obj('opposite_direction', cons)\
        or applies('to_oncoming', cons)\
        or applies_for_ego('overlap_lane', cons):
            continue

        lta = LongTrafficArtist()
        lta.draw_road()

        ego_lc_dir=None

        if applies_for_ego('lane_change', cons):

            # Get the type of lane change
            if applies_for_ego('to_left', cons) or applies('from_oncoming', cons):
                ego_lc_dir = 1
            elif applies_for_ego('to_right', cons):
                ego_lc_dir = -1
            else:
                raise ValueError('No direction for ego lane change')
            
            # Draw the lane change
            lta.draw_rel_vehicle(0,0,lta.C_EGO)
            if applies_for_ego('aborted', cons):
                lta.draw_aborted_lc(0,0,ego_lc_dir, lta.C_EGO)
            else:
                lta.draw_lc(0,0,ego_lc_dir, lta.C_EGO)
            
            if not applies_for_obj('entering', cons) \
               and applies_for_obj('in_front_of', cons):
                lta.draw_rel_vehicle(1,ego_lc_dir,lta.C_OBJ)
                lta.draw_lc(1,ego_lc_dir,0, lta.C_OBJ)
            
            if applies_for_obj('behind', cons):
                lta.draw_rel_vehicle(-1,ego_lc_dir,lta.C_OBJ)
                lta.draw_lc(-1,ego_lc_dir,0, lta.C_OBJ)

        else:
            lta.draw_rel_vehicle(0,0,lta.C_EGO)
            lta.draw_lc(0,0,0, lta.C_EGO)


        if applies_for_obj('entering', cons):
            if applies_for_obj('at_right', cons)\
               or applies_for_obj('from_right', cons):
                obj_pos = -1
                obj_dir = 1
            elif applies_for_obj('at_left', cons)\
                 or applies_for_obj('from_left', cons):
                obj_pos = 1
                obj_dir = -1
            elif applies('synchronous', cons):
                obj_pos = 0
                obj_dir = ego_lc_dir
            elif applies('merging', cons):
                obj_pos = ego_lc_dir * 2
                obj_dir = ego_lc_dir * -1
                continue
            else:
                raise AttributeError("Do direction for lane change given")

            if applies_for_obj('exiting', cons):
                obj_dir = obj_dir * 2

            lta.draw_rel_vehicle(1,obj_pos,lta.C_OBJ)
            if applies_for_obj('aborted', cons):
                lta.draw_aborted_lc(1,obj_pos,obj_dir, lta.C_OBJ)
            else:
                lta.draw_lc(1,obj_pos,obj_dir, lta.C_OBJ)
        
        elif applies_for_obj('exiting', cons):
            lta.draw_rel_vehicle(1,0,lta.C_OBJ)
            if applies_for_obj('to_right', cons):
                lta.draw_lc(1,0,-1, lta.C_OBJ)
            elif applies_for_obj('to_left', cons):
                lta.draw_lc(1,0,1, lta.C_OBJ)
            else:
                raise AttributeError("Do direction for exiting given")


        lta.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_entering_exiting(c, cons):
    lta = EnterExitArtist()
    lta.draw_road()

    lta.draw_ego(lta.C_EGO)
    lta.draw_ego_arrow(lta.C_EGO)

    if applies_for_obj('opposite_direction', cons):
        return
    if applies_for_obj('exiting', cons):
        return
    if applies_for_obj('leaving_ego_traffic_area', cons):
        draw_unique(c)

    if applies_for_obj('from_left', cons):
        near = False
    elif applies_for_obj('from_right', cons):
        near = True
    else:
        raise AttributeError('No position of ego')

    if applies_for_obj('turning', cons):
    
        if applies_for_obj('forward', cons):
            lta.draw_entering_obj_turning(near, lta.C_OBJ)
            lta.draw_entering_turn(near, lta.C_OBJ)
        elif applies_for_obj('reversing', cons):
            lta.draw_entering_obj_turning(near, lta.C_OBJ, reverse=True)
            lta.draw_entering_reversing_turn(near, lta.C_OBJ)
        else:
            raise AttributeError('No type of movement')

    elif applies_for_obj('parallel', cons):

        lta.draw_entering_obj_parallel(near, lta.C_OBJ)
    
        if applies_for_obj('forward', cons):
            lta.draw_entering_lc_forward(near, lta.C_OBJ)
        elif applies_for_obj('reversing', cons):
            lta.draw_entering_lc_reversing(near, lta.C_OBJ)
        else:
            raise AttributeError('No type of movement')

    else:
        raise AttributeError('No kind of direction.')
    
    lta.write('img/' + c.get_name(c) +'.png')
    drawn.append(c)
        
    
def draw_long_traffic_states():

    long_states = [bs for bs in base_scenarios if sce.long_traffic_state in bs.ancestors()]

    for c in long_states:

        cons = get_concepts(c)

        print(c)
        print(cons)

        # Catch the ones that need to be drawn separately
        if applies_for_obj('lateral_obj', cons):
            continue
        elif applies_for_ego('reversing', cons):
            continue
        elif applies_for_ego('standstill', cons):
            continue
        elif applies_for_obj('reversing_lead', cons):
            continue
        elif applies_for_obj('oncoming', cons):
            continue
        elif applies_for_obj('traffic_jam', cons):
            continue

        l_ego=0 if not applies_for_obj('at_right', cons) else 1

        art = LongTrafficArtist()
        art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=l_ego, n_ego=0))
        art.draw_road()

        # Draw ego
        art.draw_rel_vehicle(0,0,art.C_EGO)

        if applies_for_ego('approaching', cons):
            art.draw_approaching(0,0,art.C_EGO)
        elif applies_for_ego('following', cons) \
            or applies_for_ego('free', cons):
            art.draw_lc(0,0,0,art.C_EGO)
        else:
            raise ValueError("Not state for ego vehicle")
        
        # Draw object
        if applies_for_obj('leading', cons):
            art.draw_rel_vehicle(1,0,art.C_OBJ)
            art.draw_lc(1,0,0,art.C_OBJ)
        elif applies_for_obj('static', cons):
            art.draw_rel_vehicle(1,0,art.C_OBJ, static=True)
        elif applies_for_obj('undertaken', cons):
            art.draw_rel_vehicle(1,1,art.C_OBJ)
            art.draw_lc(1,1,0,art.C_OBJ)
        elif applies_for_obj('overlapping_object', cons):
            if applies_for_obj('at_left', cons):
                d = 0.5
            elif applies_for_obj('at_right', cons):
                d = -0.5
            else:
                raise ValueError('Got not position of overlapping object')

            art.draw_rel_vehicle(1,d,art.C_OBJ)
            art.draw_lc(1,d,0,art.C_OBJ)
        elif applies_for_ego('free', cons):
            pass
        else:
            raise ValueError("No longitudinal object")


        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_neighboring_overlays():

    overlays = [bs for bs in base_scenarios if sce.long_traffic_overlay in bs.ancestors()]

    for c in overlays:

        cons = get_concepts(c)

        print(c)
        print(cons)

        if c.get_name(c) == "close_obj_behind"\
        or c.get_name(c) == "rear_obj_approaching"\
        or c.get_name(c) == "surrounding_lc"\
        or c.get_name(c) == "passing_oncoming"\
        or applies_for_ego('being_passed_in_lane', cons)\
        or applies_for_obj('entering', cons)\
        or applies_for_obj('exiting', cons):
            continue

        art = LongTrafficArtist()

        if applies_for_obj('at_right', cons):
            l_ego = 1
            l_obj = -1
        elif applies_for_obj('at_left', cons):
            l_ego = 0
            l_obj = 1
        else:
            raise ValueError('Got no position for object.')

        if applies_for_ego('pass', cons):
            p_ego = 0
            p_obj = 1
            s_ego = 1
            e_ego = 6
            s_obj = 0.75
            e_obj = 0
        elif applies_for_ego('being_passed', cons):
            p_ego = 1
            p_obj = -1
            s_ego = 0.75
            e_ego = 0
            s_obj = 1
            e_obj = 6
        elif applies_for_ego('having_neighbor', cons):
            p_ego = 0
            p_obj = 0
            s_ego = 1
            e_ego = 2
            s_obj = 1
            e_obj = 2
        elif applies_for_ego('close_obj', cons):
            p_ego = 0
            p_obj = 0
            l_obj = 0.6 * l_obj
            s_ego = 1
            e_ego = 2
            s_obj = 1
            e_obj = 2
        else:
            raise ValueError('Got not type of relative movement')

        art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=l_ego, n_ego=p_ego, car_spacing=1, margin=4))
        art.draw_road()

        art.draw_rel_vehicle(0,0,art.C_EGO)
        art.draw_scaled_arrow(0,0,art.C_EGO, extension=e_ego, scaling=s_ego)

        art.draw_rel_vehicle(p_obj, l_obj, art.C_OBJ)
        art.draw_scaled_arrow(p_obj, l_obj, art.C_OBJ, extension=e_obj, scaling=s_obj)

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


# TODO Approach laterally moving object crossing / entering
def draw_approach_lat():
    approach_lats = [bs for bs in base_scenarios if sce.approach_lat in bs.ancestors()]

    for c in approach_lats:

        cons = get_concepts(c)

        print(c)
        print(cons)

        if c.get_name(c) == "approach_lat_entering_traffic_area_from_left"\
        or applies_for_obj('leaving_ego_traffic_area', cons):
            continue

        art = EnterExitArtist()
        art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=1))
        art.draw_road()

        art.draw_ego(art.C_EGO)
        art.draw_ego_arrow(art.C_EGO)

        if applies_for_obj('from_left', cons):
            near = False
        elif applies_for_obj('from_right', cons):
            near = True
        else:
            raise ValueError('No position of object defined.')

        if applies_for_obj('cross_ego_traffic_area', cons):
            art.draw_entering_vru(near, art.C_OBJ)
            art.draw_crossing(near, art.C_OBJ)
        elif applies_for_obj('enter_ego_traffic_area', cons):
            art.draw_entering_obj_turning(near, art.C_OBJ)
            if applies_for_obj('same_direction', cons):
                art.draw_crossing_turn(near, False, art.C_OBJ)
            elif applies_for_obj('opposite_direction', cons):
                art.draw_crossing_turn(near, True, art.C_OBJ)
            else:
                raise ValueError('No direction for entering.')
        else:
            raise ValueError('No movement of object defined.')
        
        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)
            

def draw_exit_leaving_ego_TA():

    exits = [bs for bs in base_scenarios if sce.exit_leaving_ego_TA in bs.ancestors()]

    for c in exits:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = EnterExitArtist()

        art.set_road(LongTraffic(n_lanes=2, n_pos=2, l_ego=0, n_ego=0))

        art.draw_road()

        art.draw_ego(art.C_EGO)
        art.draw_ego_arrow(art.C_EGO)

        art.draw_exiting_leading_obj(art.C_OBJ)

        if applies_for_obj('to_left', cons):
            near = False
        elif applies_for_obj('to_right', cons):
            near = True
        else:
            raise AttributeError('No position of ego')

        if applies_for_obj('turning', cons):
        
            if applies_for_obj('forward', cons):
                art.draw_exiting_turn_forward(near, art.C_OBJ)
            elif applies_for_obj('reversing', cons):
                art.draw_exiting_turn_reversing(near, art.C_OBJ)
            else:
                raise AttributeError('No type of movement')

        elif applies_for_obj('parallel', cons):
            if applies_for_obj('forward', cons):
                art.draw_exiting_lc_forward(near, art.C_OBJ)
            elif applies_for_obj('reversing', cons):
                art.draw_exiting_lc_reversing(near, art.C_OBJ)
            else:
                raise AttributeError('No type of movement')

        else:
            raise AttributeError('No kind of direction.')
        
        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_overlap_lane():

    overlapping = [bs for bs in base_scenarios if sce.overlap_lane in bs.ancestors()]

    for c in overlapping:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = LongTrafficArtist()
        if applies_for_ego('at_left', cons):
            ol = 0.35
            art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0, n_ego=0))
        elif applies_for_ego('at_right', cons):
            ol = -0.35
            art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=1, n_ego=0))
        else:
            raise ValueError('No overlap direction.')
        
        art.draw_road()

        # Draw ego
        art.draw_rel_vehicle(0,ol,art.C_EGO)

        if applies_for_obj('leading', cons):
            if applies_for_ego('following', cons):
                art.draw_scaled_arrow(0,ol,art.C_EGO)
                art.draw_rel_vehicle(1,ol,art.C_OBJ)
                art.draw_scaled_arrow(1,ol,art.C_OBJ)
            elif applies_for_ego('approaching', cons):
                art.draw_approaching(0,ol,art.C_EGO)
                art.draw_rel_vehicle(1,ol,art.C_OBJ)
                art.draw_scaled_arrow(1,ol,art.C_OBJ)
            else:
                raise ValueError('No relation to leading object')
        else:
            art.draw_scaled_arrow(0,ol,art.C_EGO)

        if applies_for_obj('oncoming', cons):
            art.draw_rel_vehicle(2,1,art.C_OBJ, oncoming=True)
            art.draw_reverse_lc(2,1,0,art.C_OBJ)

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_lane_change_with_oncoming():

    overlapping = [bs for bs in base_scenarios if sce.lane_change in bs.ancestors()
                                 and sce.transition_with_oncoming in bs.ancestors()]

    for c in overlapping:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = LongTrafficArtist()
        art.set_road(LongTraffic(n_lanes=2, n_pos=3, l_ego=0))#
        art.draw_road()

        if applies('to_oncoming', cons):
            l_ego = 0
            d_ego = 1
        elif applies('from_oncoming', cons):
            l_ego = 1
            d_ego = -1
        else:
            raise ValueError('No relation to oncoming.')
        
        art.draw_rel_vehicle(0,l_ego,art.C_EGO)
        art.draw_lc(0,l_ego,d_ego,art.C_EGO)

        art.draw_rel_vehicle(2,1,art.C_OBJ,oncoming=True)
        art.draw_reverse_arrow(2,1,art.C_OBJ)

        if applies_for_obj('behind', cons):
            art.draw_rel_vehicle(-1,l_ego+d_ego,art.C_OBJ)
            art.draw_lc(-1,l_ego+d_ego,0, art.C_OBJ)

        if applies_for_obj('in_front_of', cons):
            art.draw_rel_vehicle(1,l_ego+d_ego,art.C_OBJ)
            art.draw_lc(1,l_ego+d_ego,0, art.C_OBJ)

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_non_parallel_intersection_overlays():

    overlays = [bs for bs in base_scenarios if sce.pass_obj_in_intersection_moving_away in bs.ancestors()
                   or sce.pass_obj_in_intersection_moving_toward in bs.ancestors()]

    for c in overlays:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = IntersectionArtist()
        art.draw_intersection()

        ex = 3

        if applies_for_obj('towards', cons):

            if applies_for_obj('at_right', cons):
                if applies_for_obj('left_turn', cons):
                    art.draw_partial_left_turn('e', art.C_OBJ, partial=0, extension=ex)
                elif applies_for_obj('right_turn', cons):
                    art.draw_partial_right_turn('e', art.C_OBJ, partial=0, extension=ex)
                elif applies_for_obj('passing_straight', cons):
                    art.draw_partial_passing_straight('e', art.C_OBJ, partial=0, extension=ex)
                elif applies_for_obj('u-turn', cons):
                    art.draw_partial_u_turn('e', art.C_OBJ, partial=0, extension=ex)
                
                art.draw_entering_vehicle('e', art.C_OBJ)
                art.draw_passing_vehicle('s', art.C_EGO, offset=.5)
            
            elif applies_for_obj('at_left', cons):
                if applies_for_obj('left_turn', cons):
                    art.draw_partial_left_turn('w', art.C_OBJ, partial=0, extension=ex)
                elif applies_for_obj('right_turn', cons):
                    art.draw_partial_right_turn('w', art.C_OBJ, partial=0, extension=ex)
                elif applies_for_obj('passing_straight', cons):
                    art.draw_partial_passing_straight('w', art.C_OBJ, partial=0, extension=ex)
                elif applies_for_obj('u-turn', cons):
                    art.draw_partial_u_turn('w', art.C_OBJ, partial=0, extension=ex)
                
                art.draw_entering_vehicle('w', art.C_OBJ)            
                art.draw_passing_vehicle('s', art.C_EGO, offset=-.5)

        elif applies_for_obj('away', cons):

            if applies_for_obj('at_right', cons):
                if applies_for_obj('left_turn', cons):
                    (p,h) = art.draw_partial_left_turn('n', art.C_OBJ, partial=1, extension=ex)
                elif applies_for_obj('right_turn', cons):
                    (p,h) = art.draw_partial_right_turn('s', art.C_OBJ, partial=1, extension=ex)
                elif applies_for_obj('passing_straight', cons):
                    (p,h) = art.draw_partial_passing_straight('w', art.C_OBJ, partial=1, extension=ex)
                elif applies_for_obj('u-turn', cons):
                    (p,h) = art.draw_partial_u_turn('e', art.C_OBJ, partial=1, extension=ex)
                
                art.draw_vehicle(p, h, art.C_OBJ)
                art.draw_passing_vehicle('s', art.C_EGO, offset=-.5, lat=-.3)
            
            elif applies_for_obj('at_left', cons):
                if applies_for_obj('left_turn', cons):
                    (p,h) = art.draw_partial_left_turn('s', art.C_OBJ, partial=0.8, extension=ex)
                elif applies_for_obj('right_turn', cons):
                    (p,h) = art.draw_partial_right_turn('n', art.C_OBJ, partial=0.8, extension=ex)
                elif applies_for_obj('passing_straight', cons):
                    (p,h) = art.draw_partial_passing_straight('e', art.C_OBJ, partial=0.8, extension=ex)
                elif applies_for_obj('u-turn', cons):
                    (p,h) = art.draw_partial_u_turn('w', art.C_OBJ, partial=0.8, extension=ex)
                
                art.draw_vehicle(p, h, art.C_OBJ)           
                art.draw_passing_vehicle('s', art.C_EGO, offset=.5)

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_parallel_entry():

    overlapping = [bs for bs in base_scenarios if sce.conflict_with_parallel_entry in bs.ancestors()]

    for c in overlapping:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = ComplexArtist()

        art.draw_intersection()

        if applies_for_obj('at_left', cons):
            lane_ego = 0
            lane_obj = 1
        elif applies_for_obj('at_right', cons):
            lane_ego = 1
            lane_obj = 0
        else:
            raise ValueError('No position of object')
        
        p_ego = art.road.get_entry('s', lane_ego)
        art.draw_vehicle(p_ego, mirror('s'), art.C_EGO)

        if applies_for_ego('left_turn', cons):
            art.draw_left_turn('s', art.C_EGO, l=lane_ego)
        elif applies_for_ego('right_turn', cons):
            art.draw_right_turn('s', art.C_EGO, l=lane_ego)
        elif applies_for_ego('passing_straight', cons):
            art.draw_passing_straight('s', art.C_EGO, l=lane_ego)
        else:
            raise ValueError('No maneuver for ego')

        p_obj = art.road.get_entry('s', lane_obj)
        art.draw_vehicle(p_obj, mirror('s'),art.C_OBJ)
        
        if applies_for_obj('left_turn', cons):
            art.draw_left_turn('s', art.C_OBJ, l=lane_obj)
        elif applies_for_obj('right_turn', cons):
            art.draw_right_turn('s', art.C_OBJ, l=lane_obj)
        elif applies_for_obj('passing_straight', cons):
            art.draw_passing_straight('s', art.C_OBJ, l=lane_obj)
        elif applies_for_obj('u-turn', cons):
            art.draw_u_turn('s', art.C_OBJ, l=lane_obj)
        else:
            raise ValueError('No maneuver for obj')

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_parallel_overlays():

    overlays = [bs for bs in base_scenarios if sce.parallel_intersection_overlay in bs.ancestors()]

    for c in overlays:

        cons = get_concepts(c)

        if c.get_name(c) == "passing_oncoming_in_intersection":
            continue

        print(c)
        print(cons)

        art = ComplexArtist()

        art.draw_intersection()

        if applies_for_obj('at_left', cons):
            lane_ego = 0
            lane_obj = 1
        elif applies_for_obj('at_right', cons):
            lane_ego = 1
            lane_obj = 0
        else:
            raise ValueError('No position of object')
        
        art.draw_partial_left_turn('s', art.C_EGO, partial=1, l=lane_ego)
        art.draw_partial_left_turn('s', art.C_OBJ, partial=1, l=lane_obj)
        art.draw_partial_right_turn('s', art.C_EGO, partial=1, l=lane_ego)
        art.draw_partial_right_turn('s', art.C_OBJ, partial=1, l=lane_obj)
        art.draw_partial_u_turn('s', art.C_EGO, partial=1, l=lane_ego)
        art.draw_partial_u_turn('s', art.C_OBJ, partial=1, l=lane_obj)
        
        if applies_for_ego('pass', cons):
            (p_ego, h_ego) = art.draw_partial_passing_straight('s', art.C_EGO, partial=0.3, extension=3, l=lane_ego)
            (p_obj, h_obj) = art.draw_partial_passing_straight('s', art.C_OBJ, partial=0.5, extension=0, l=lane_obj)
        elif applies_for_ego('being_passed', cons):
            (p_ego, h_ego) = art.draw_partial_passing_straight('s', art.C_EGO, partial=0.5, extension=0, l=lane_ego)
            (p_obj, h_obj) = art.draw_partial_passing_straight('s', art.C_OBJ, partial=0.3, extension=3, l=lane_obj)
        elif applies_for_ego('having_neighbor', cons):
            (p_ego, h_ego) = art.draw_partial_passing_straight('s', art.C_EGO, partial=0.5, extension=1, l=lane_ego)
            (p_obj, h_obj) = art.draw_partial_passing_straight('s', art.C_OBJ, partial=0.5, extension=1, l=lane_obj)
        elif applies_for_ego('close_obj', cons):
            continue  # These are drawn as unique
        else:
            raise ValueError('No relation to obj')
        
        art.draw_vehicle(p_ego, h_ego, art.C_EGO)
        art.draw_vehicle(p_obj, h_obj, art.C_OBJ)

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_intersection_states():

    states = [bs for bs in base_scenarios if sce.intersection_state in bs.ancestors()
                                          and not sce.standstill_in_intersection in bs.ancestors()]

    for c in states:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = ComplexArtist()

        art = ComplexArtist()

        START_EGO = 0
        END_EGO = 0.4
        START_OBJ = 0.7
        END_OBJ = 1
        EX = 3

        if applies_for_ego('left_turn', cons):
            maneuver_func = art.draw_incomplete_left_turn
            lane = 1
        elif applies_for_ego('right_turn', cons):
            maneuver_func = art.draw_incomplete_right_turn
            lane = 1
        elif applies_for_ego('passing_straight', cons):
            maneuver_func = art.draw_incomplete_passing_straight
            lane = 0
        elif applies_for_ego('u-turn', cons):
            maneuver_func = art.draw_incomplete_u_turn
            lane = 0
        else:
            raise ValueError('Got no maneuver for ego')
        
        art.draw_intersection()
        art.draw_entering_vehicle('s', art.C_EGO, l=lane)

        if applies_for_ego('free', cons):
            maneuver_func('s', art.C_EGO, start=START_EGO, end=END_OBJ, extension=EX, double=False, l=lane)
        elif applies_for_ego('following', cons):
            maneuver_func('s', art.C_EGO, start=START_EGO, end=END_EGO, extension=EX, double=False, l=lane)
            (p_obj, h_obj) = maneuver_func('s', art.C_EGO, start=0, end=START_OBJ, extension=EX, invis=True, l=lane)
            maneuver_func('s', art.C_OBJ, start=START_OBJ, end=END_OBJ, extension=EX, invis=False, double=False, l=lane)
            art.draw_vehicle(p_obj, h_obj, art.C_OBJ)
        elif applies_for_ego('approaching', cons):
            if applies_for_obj('leading', cons):
                maneuver_func('s', art.C_EGO, start=START_EGO, end=END_EGO, extension=EX, double=True, l=lane)
                (p_obj, h_obj) = maneuver_func('s', art.C_EGO, start=0, end=START_OBJ, extension=EX, invis=True, l=lane)
                maneuver_func('s', art.C_OBJ, start=START_OBJ, end=END_OBJ, extension=EX, invis=False, double=False, l=lane)
                art.draw_vehicle(p_obj, h_obj, art.C_OBJ)
            elif applies_for_obj('static', cons):
                maneuver_func('s', art.C_EGO, start=START_EGO, end=END_EGO, extension=EX, double=True, l=lane)
                (p_obj, h_obj) = maneuver_func('s', art.C_EGO, start=0, end=START_OBJ, extension=EX, invis=True, l=lane)
                art.draw_static(p_obj, h_obj, art.C_OBJ)
            else:
                raise ValueError('Do not know the type of object')
        else:
            raise ValueError('Got no relation to object')

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_intersection_standstill():
    
    standstills = [bs for bs in base_scenarios if sce.standstill_in_intersection in bs.ancestors()]

    for c in standstills:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = ComplexArtist()

        art.draw_intersection()

        if applies_for_ego('left_turn', cons):
            lane = 1
            (p_ego, h_ego) = art.draw_partial_left_turn('s', art.C_EGO, 0.5, 3, l=lane)
        elif applies_for_ego('right_turn', cons):
            lane = 1
            (p_ego, h_ego) = art.draw_partial_right_turn('s', art.C_EGO, 0.5, 3, l=lane)
        elif applies_for_ego('passing_straight', cons):
            lane = 0
            (p_ego, h_ego) = art.draw_partial_passing_straight('s', art.C_EGO, 0.5, 3, l=lane)
        elif applies_for_ego('u-turn', cons):
            lane = 0
            (p_ego, h_ego) = art.draw_partial_u_turn('s', art.C_EGO, 0.5, 3, l=lane)
        else:
            raise ValueError('Got no maneuver for ego')
        
        art.draw_static(p_ego, h_ego, art.C_EGO)

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)

def draw_reversing():

    standstills = [bs for bs in base_scenarios if sce.reverse in bs.ancestors()
                   and not sce.reverse_approach_lat in bs.ancestors()]

    for c in standstills:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = LongTrafficArtist()
        art.set_road(LongTraffic(n_pos=2, l_ego=0, n_lanes=2, n_ego=1, front_space=False))
        art._setup_context()

        art.draw_road()
        art.draw_rel_vehicle(0,0,art.C_EGO)
        art.draw_reverse_arrow(0,0,art.C_EGO, scaling=0.3)

        if applies_for_obj('static', cons):
            art.draw_rel_vehicle(-1,0,art.C_OBJ,static=True)
        elif applies_for_obj('oncoming', cons):
            art.draw_rel_vehicle(-1,0,art.C_OBJ)
            art.draw_scaled_arrow(-1,0,art.C_OBJ, 0.7)
        elif applies_for_ego('free', cons):
            pass
        else:
            raise ValueError('Do not know the driving ')

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_rear_obj_transitions():

    overlays = [bs for bs in base_scenarios if sce.rear_obj_entering in bs.ancestors()
                    or sce.rear_obj_exiting in bs.ancestors()]

    for c in overlays:

        cons = get_concepts(c)

        print(c)
        print(cons)

        art = LongTrafficArtist()
        art.set_road(LongTraffic(n_lanes=3, l_ego=1, n_pos=2, n_ego=1))

        art.draw_road()

        art.draw_rel_vehicle(0,0,art.C_EGO)
        art.draw_lc(0,0,0,art.C_EGO)

        if applies_for_obj('entering', cons):
            if applies_for_obj('from_left', cons):
                art.draw_rel_vehicle(-1,1,art.C_OBJ)
                art.draw_lc(-1,1,-1,art.C_OBJ)
            elif applies_for_obj('from_right', cons):
                art.draw_rel_vehicle(-1,-1,art.C_OBJ)
                art.draw_lc(-1,-1,1,art.C_OBJ)
            else:
                raise ValueError('Got not direction for obj')
        elif applies_for_obj('exiting', cons):
            if applies_for_obj('to_left', cons):
                art.draw_rel_vehicle(-1,0,art.C_OBJ)
                art.draw_lc(-1,0,1,art.C_OBJ)
            elif applies_for_obj('to_right', cons):
                art.draw_rel_vehicle(-1,0,art.C_OBJ)
                art.draw_lc(-1,0,-1,art.C_OBJ)
            else:
                raise ValueError('Got not direction for obj')
        else:
            raise ValueError('Got not transition for obj')

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def draw_neighbor_transitions():

    overlays = [bs for bs in base_scenarios if sce.neighbor_entering in bs.ancestors()
                    or sce.neighbor_exiting in bs.ancestors()]

    for c in overlays:

        cons = get_concepts(c)

        print(c)
        print(cons)

        if applies_for_obj('entering', cons):
            if applies_for_obj('at_left', cons):
                l_ego = 0
                d_obj = -1
            elif applies_for_obj('at_right', cons):
                l_ego = 2
                d_obj = 1
            else:
                raise ValueError('Got not direction for obj')
            l_obj = - d_obj*2
        elif applies_for_obj('exiting', cons):
            if applies_for_obj('to_left', cons):
                l_ego = 0
                d_obj = 1
            elif applies_for_obj('to_right', cons):
                l_ego = 2
                d_obj = -1
            else:
                raise ValueError('Got not direction for obj')
            l_obj = d_obj
        else:
            raise ValueError('Got not transition for obj')

        art = LongTrafficArtist()
        art.set_road(LongTraffic(n_lanes=3, l_ego=l_ego, n_pos=2, n_ego=1))

        art.draw_road()

        art.draw_rel_vehicle(0,0,art.C_EGO)
        art.draw_lc(0,0,0,art.C_EGO)
        art.draw_rel_vehicle(0,l_obj,art.C_OBJ)
        art.draw_lc(0,l_obj,d_obj,art.C_OBJ)

        art.write('img/' + c.get_name(c) +'.png')
        drawn.append(c)


def get_concepts(bs):
    parents = bs.ancestors()
    cons = []
    for p in parents:
        if isinstance(p, owl.class_construct.Restriction):
            print("Got a base scenario concept. This is unexpected")
            cons.append((p.property.get_name(), p.value.get_name(p.value)))
        elif isinstance(p, owl.entity.ThingClass):
            ps_parents = p.is_a
            con = []
            for pp in ps_parents:
                if isinstance(pp, owl.class_construct.Restriction):
                    con.append((pp.property.get_name(), pp.value.get_name(pp.value)))
            if con:
                cons.extend(con)
            else:
                print("Got not concept for "+p.get_name(p))
    return cons


def applies(what, in_what):
    # Check if it is in concepts at all
    if not what in concept_names:
        raise ValueError(f"{what} is not a valid concept")
    
    if isinstance(what, str):
        what = [what]
    
    # Check if any of the supplied concepts is in
    for w in what:
        if ('applies', w) in in_what:
            return True
    
    # If we land here it is false
    return False


def applies_for_ego(what, in_what):
    # Check if it is in concepts at all
    if not what in concept_names:
        raise ValueError(f"{what} is not a valid concept")

    if isinstance(what, str):
        what = [what]
    
    # Check if any of the supplied concepts is in
    for w in what:
        if ('applies_for_ego', w) in in_what:
            return True
    
    # If we land here it is false
    return False

def applies_for_obj(what, in_what):
    # Check if it is in concepts at all
    if not what in concept_names:
        raise ValueError(f"{what} is not a valid concept")
    
    if isinstance(what, str):
        what = [what]
    
    # Check if any of the supplied concepts is in
    for w in what:
        if ('applies_for_obj', w) in in_what:
            return True
    
    # If we land here it is false
    return False


def draw_incomplete_enter_lead():
    pass


if __name__ == "__main__":
    main()


