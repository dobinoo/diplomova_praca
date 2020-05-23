import math                     #math library for pow,sqrt,degrees ..
import numpy as np              #also mathematical library but this works with arctan (math library had problem with arctan)
from flask_server import *        #importing server file to get all globals


#if ever needed polar to cartesian convertion
def polar_to_cartesian(r,phi):
    #x = r * cos(phi)
    #y = r * sin(phi)

    x = r * math.cos(math.radians(phi-90))      #we need to substract 90 bc of uArm
    x = round(x)

    y = r * math.sin(math.radians(phi-90))      #we need to substract 90 bc of uArm
    y = round(y)

    return x,y                                  #returning two values

#cartesian to polar convertion
def cartesian_to_polar(x,y):
    # r = sqrt(x^2 + y^2)
    # phi = tan^-1(y/x)

    #stretch (distance between start and end)
    r = math.sqrt(pow(x,2) + pow(y,2))
    r = round(r)

    # rotation(angle)
    phi = np.arctan2(y,x)
    phi = math.degrees(phi) + 90
    phi = round(phi)
    return r, phi                               #returning two values

#cartesian to polar coordinates
def change_variables_to_polar():

    #cartesian coordinates
    global robot_pos1_pick_x, robot_pos1_pick_y, robot_pos1_pick_z, robot_pos1_drop_x, robot_pos1_drop_y, robot_pos1_drop_z
    global robot_pos2_pick_x, robot_pos2_pick_y, robot_pos2_pick_z, robot_pos2_drop_x, robot_pos2_drop_y, robot_pos2_drop_z
    global robot_pos3_pick_x, robot_pos3_pick_y, robot_pos3_pick_z, robot_pos3_drop_x, robot_pos3_drop_y, robot_pos3_drop_z
    global default_x, default_y, default_z

    #polar coordinates
    global robot_pos1_pick_stretch, robot_pos1_pick_rotate, robot_pos1_pick_height, robot_pos1_drop_stretch, robot_pos1_drop_rotate, robot_pos1_drop_height
    global robot_pos2_pick_stretch, robot_pos2_pick_rotate, robot_pos2_pick_height, robot_pos2_drop_stretch, robot_pos2_drop_rotate, robot_pos2_drop_height
    global robot_pos3_pick_stretch, robot_pos3_pick_rotate, robot_pos3_pick_height, robot_pos3_drop_stretch, robot_pos3_drop_rotate, robot_pos3_drop_height
    global default_stretch, default_rotation, default_height

    #coordinates for default position of robot
    result = cartesian_to_polar(default_x,default_y)
    default_stretch = result[0]
    default_rotation = result[1]
    default_height = default_z

    #coordinates for pos1 pick
    result = cartesian_to_polar(robot_pos1_pick_x,robot_pos1_pick_y)
    robot_pos1_pick_stretch = result[0]
    robot_pos1_pick_rotate = result[1]
    robot_pos1_pick_height = robot_pos1_pick_z

    #coordinates for pos1 drop
    result = cartesian_to_polar(robot_pos1_drop_x,robot_pos1_drop_y)
    robot_pos1_drop_stretch = result[0]
    robot_pos1_drop_rotate = result[1]
    robot_pos1_drop_height = robot_pos1_drop_z

    #coordinates for pos2 pick
    result = cartesian_to_polar(robot_pos2_pick_x,robot_pos2_pick_y)
    robot_pos2_pick_stretch = result[0]
    robot_pos2_pick_rotate = result[1]
    robot_pos2_pick_height = robot_pos2_pick_z

    #coordinates for pos2 drop
    result = cartesian_to_polar(robot_pos2_drop_x,robot_pos2_drop_y)
    robot_pos2_drop_stretch = result[0]
    robot_pos2_drop_rotate = result[1]
    robot_pos2_drop_height = robot_pos2_drop_z

    #coordinates for pos3 pick
    result = cartesian_to_polar(robot_pos3_pick_x,robot_pos3_pick_y)
    robot_pos3_pick_stretch = result[0]
    robot_pos3_pick_rotate = result[1]
    robot_pos3_pick_height = robot_pos3_pick_z

    #coordinates for pos3 drop
    result = cartesian_to_polar(robot_pos3_drop_x,robot_pos3_drop_y)
    robot_pos3_drop_stretch = result[0]
    robot_pos3_drop_rotate = result[1]
    robot_pos3_drop_height = robot_pos3_drop_z

    return

def change_variables_to_cartesian():

    #cartesian coordinates
    global robot_pos1_pick_x, robot_pos1_pick_y, robot_pos1_pick_z, robot_pos1_drop_x, robot_pos1_drop_y, robot_pos1_drop_z
    global robot_pos2_pick_x, robot_pos2_pick_y, robot_pos2_pick_z, robot_pos2_drop_x, robot_pos2_drop_y, robot_pos2_drop_z
    global robot_pos3_pick_x, robot_pos3_pick_y, robot_pos3_pick_z, robot_pos3_drop_x, robot_pos3_drop_y, robot_pos3_drop_z
    global default_x, default_y, default_z

    #polar coordinates
    global robot_pos1_pick_stretch, robot_pos1_pick_rotate, robot_pos1_pick_height, robot_pos1_drop_stretch, robot_pos1_drop_rotate, robot_pos1_drop_height
    global robot_pos2_pick_stretch, robot_pos2_pick_rotate, robot_pos2_pick_height, robot_pos2_drop_stretch, robot_pos2_drop_rotate, robot_pos2_drop_height
    global robot_pos3_pick_stretch, robot_pos3_pick_rotate, robot_pos3_pick_height, robot_pos3_drop_stretch, robot_pos3_drop_rotate, robot_pos3_drop_height
    global default_stretch, default_rotation, default_height

    #coordinates for default position of robot
    result = polar_to_cartesian(default_stretch,default_rotation)
    default_x = result[0]
    default_y = result[1]
    default_z = default_height

    #coordinates for pos1 pick
    result = polar_to_cartesian(robot_pos1_pick_stretch,robot_pos1_pick_rotate)
    robot_pos1_pick_x = result[0]
    robot_pos1_pick_y = result[1]
    robot_pos1_pick_z = robot_pos1_pick_height

    #coordinates for pos1 drop
    result = polar_to_cartesian(robot_pos1_drop_stretch,robot_pos1_drop_rotate)
    robot_pos1_drop_x = result[0]
    robot_pos1_drop_y = result[1]
    robot_pos1_drop_z = robot_pos1_drop_height

    #coordinates for pos2 pick
    result = polar_to_cartesian(robot_pos2_pick_stretch,robot_pos2_pick_rotate)
    robot_pos2_pick_x = result[0]
    robot_pos2_pick_y = result[1]
    robot_pos2_pick_z = robot_pos2_pick_height

    #coordinates for pos2 drop
    result = polar_to_cartesian(robot_pos2_drop_stretch,robot_pos2_drop_rotate)
    robot_pos2_drop_x = result[0]
    robot_pos2_drop_y = result[1]
    robot_pos2_drop_z = robot_pos2_drop_height

    #coordinates for pos3 pick
    result = polar_to_cartesian(robot_pos3_pick_stretch,robot_pos3_pick_rotate)
    robot_pos3_pick_x = result[0]
    robot_pos3_pick_y = result[1]
    robot_pos3_pick_z = robot_pos3_pick_height

    #coordinates for pos3 drop
    result = polar_to_cartesian(robot_pos3_drop_stretch,robot_pos3_drop_rotate)
    robot_pos3_drop_x = result[0]
    robot_pos3_drop_y = result[1]
    robot_pos3_drop_z = robot_pos3_drop_height

    return

#test function that convertion works fine
def test_converting(cartesian):
    correct = True

    #cartesian coordinates
    global robot_pos1_pick_x, robot_pos1_pick_y, robot_pos1_pick_z, robot_pos1_drop_x, robot_pos1_drop_y, robot_pos1_drop_z
    global robot_pos2_pick_x, robot_pos2_pick_y, robot_pos2_pick_z, robot_pos2_drop_x, robot_pos2_drop_y, robot_pos2_drop_z
    global robot_pos3_pick_x, robot_pos3_pick_y, robot_pos3_pick_z, robot_pos3_drop_x, robot_pos3_drop_y, robot_pos3_drop_z
    global default_x, default_y, default_z

    #polar coordinates
    global robot_pos1_pick_stretch, robot_pos1_pick_rotate, robot_pos1_pick_height, robot_pos1_drop_stretch, robot_pos1_drop_rotate, robot_pos1_drop_height
    global robot_pos2_pick_stretch, robot_pos2_pick_rotate, robot_pos2_pick_height, robot_pos2_drop_stretch, robot_pos2_drop_rotate, robot_pos2_drop_height
    global robot_pos3_pick_stretch, robot_pos3_pick_rotate, robot_pos3_pick_height, robot_pos3_drop_stretch, robot_pos3_drop_rotate, robot_pos3_drop_height
    global default_stretch, default_rotation, default_height

    #cartesian coordinates
    cartesian_pos1 = [robot_pos1_pick_x, robot_pos1_pick_y, robot_pos1_pick_z, robot_pos1_drop_x, robot_pos1_drop_y, robot_pos1_drop_z]
    cartesian_pos2 = [robot_pos2_pick_x, robot_pos2_pick_y, robot_pos2_pick_z, robot_pos2_drop_x, robot_pos2_drop_y, robot_pos2_drop_z]
    cartesian_pos3 = [robot_pos3_pick_x, robot_pos3_pick_y, robot_pos3_pick_z, robot_pos3_drop_x, robot_pos3_drop_y, robot_pos3_drop_z]
    cartesian_default = [default_x, default_y, default_z]

    #polar coordinates
    polar_pos1 = [robot_pos1_pick_stretch, robot_pos1_pick_rotate, robot_pos1_pick_height, robot_pos1_drop_stretch, robot_pos1_drop_rotate, robot_pos1_drop_height]
    polar_pos2 = [robot_pos2_pick_stretch, robot_pos2_pick_rotate, robot_pos2_pick_height, robot_pos2_drop_stretch, robot_pos2_drop_rotate, robot_pos2_drop_height]
    polar_pos3 = [robot_pos3_pick_stretch, robot_pos3_pick_rotate, robot_pos3_pick_height, robot_pos3_drop_stretch, robot_pos3_drop_rotate, robot_pos3_drop_height]
    polar_default = [default_stretch, default_rotation, default_height]

    #test
    if(cartesian):
        change_variables_to_cartesian()     #from polar to cartesian
        change_variables_to_polar()         #from cartesian to polar

        #acquire newly calculated values
        new_polar_pos1 = [robot_pos1_pick_stretch, robot_pos1_pick_rotate, robot_pos1_pick_height, robot_pos1_drop_stretch, robot_pos1_drop_rotate, robot_pos1_drop_height]
        new_polar_pos2 = [robot_pos2_pick_stretch, robot_pos2_pick_rotate, robot_pos2_pick_height, robot_pos2_drop_stretch, robot_pos2_drop_rotate, robot_pos2_drop_height]
        new_polar_pos3 = [robot_pos3_pick_stretch, robot_pos3_pick_rotate, robot_pos3_pick_height, robot_pos3_drop_stretch, robot_pos3_drop_rotate, robot_pos3_drop_height]
        new_polar_default = [default_stretch, default_rotation, default_height]

        #compare old and new value (should be same)
        for i in list(range(3)):
            if(polar_default[i] != new_polar_default[i]):
                print(i)
                print("Old polar default",polar_default[i])
                print("New polar default",new_polar_default[i])
                correct = False

        for i in list(range(6)):
            if(polar_pos1[i] != new_polar_pos1[i]):
                print(i)
                print("Old polar",polar_pos1[i])
                print("New polar",new_polar_pos1[i])
                correct = False

        for i in list(range(6)):
            if(polar_pos2[i] != new_polar_pos2[i]):
                print(i)
                print("Old polar2",polar_pos2[i])
                print("New polar2",new_polar_pos2[i])
                correct = False

        for i in list(range(6)):
            if(polar_pos3[i] != new_polar_pos3[i]):
                print(i)
                print("Old polar3",polar_pos3[i])
                print("New polar3",new_polar_pos3[i])
                correct = False
    else:
        change_variables_to_polar()         #from cartesian to polar
        change_variables_to_cartesian()     #from polar to cartesian

        new_cartesian_pos1 = [robot_pos1_pick_x, robot_pos1_pick_y, robot_pos1_pick_z, robot_pos1_drop_x, robot_pos1_drop_y, robot_pos1_drop_z]
        new_cartesian_pos2 = [robot_pos2_pick_x, robot_pos2_pick_y, robot_pos2_pick_z, robot_pos2_drop_x, robot_pos2_drop_y, robot_pos2_drop_z]
        new_cartesian_pos3 = [robot_pos3_pick_x, robot_pos3_pick_y, robot_pos3_pick_z, robot_pos3_drop_x, robot_pos3_drop_y, robot_pos3_drop_z]
        new_cartesian_default = [default_x, default_y, default_z]

        #compare old and new value (should be same)
        for i in list(range(3)):
            if(cartesian_default[i] != new_cartesian_default[i]):
                print(i)
                print("Old cartesian default",cartesian_default[i])
                print("New cartesian default",new_cartesian_default[i])
                correct = False

        for i in list(range(6)):
            if(cartesian_pos1[i] != new_cartesian_pos1[i]):
                print(i)
                print("Old cartesian",cartesian_pos1[i])
                print("New cartesian",new_cartesian_pos1[i])
                correct = False

        for i in list(range(6)):
            if(cartesian_pos2[i] != new_cartesian_pos2[i]):
                print(i)
                print("Old cartesian2",cartesian_pos2[i])
                print("New cartesian2",new_cartesian_pos2[i])
                correct = False

        for i in list(range(6)):
            if(cartesian_pos3[i] != new_cartesian_pos3[i]):
                print(i)
                print("Old cartesian3",cartesian_pos3[i])
                print("New cartesian3",new_cartesian_pos3[i])
                correct = False

    #after test complete setting to cartesian default values
    robot_pos1_pick_x = cartesian_pos1[0]
    robot_pos1_pick_y = cartesian_pos1[1]
    robot_pos1_pick_z = cartesian_pos1[2]
    robot_pos1_drop_x = cartesian_pos1[3]
    robot_pos1_drop_y = cartesian_pos1[4]
    robot_pos1_drop_z = cartesian_pos1[5]

    robot_pos2_pick_x = cartesian_pos2[0]
    robot_pos2_pick_y = cartesian_pos2[1]
    robot_pos2_pick_z = cartesian_pos2[2]
    robot_pos2_drop_x = cartesian_pos2[3]
    robot_pos2_drop_y = cartesian_pos2[4]
    robot_pos2_drop_z = cartesian_pos2[5]

    robot_pos3_pick_x = cartesian_pos3[0]
    robot_pos3_pick_y = cartesian_pos3[1]
    robot_pos3_pick_z = cartesian_pos3[2]
    robot_pos3_drop_x = cartesian_pos3[3]
    robot_pos3_drop_y = cartesian_pos3[4]
    robot_pos3_drop_z = cartesian_pos3[5]

    default_x = cartesian_default[0]
    default_y = cartesian_default[1]
    default_z = cartesian_default[2]

    #after test complete setting to polar default values
    robot_pos1_pick_stretch = polar_pos1[0]
    robot_pos1_pick_rotate = polar_pos1[1]
    robot_pos1_pick_height = polar_pos1[2]
    robot_pos1_drop_stretch = polar_pos1[3]
    robot_pos1_drop_rotate = polar_pos1[4]
    robot_pos1_drop_height = polar_pos1[5]

    robot_pos2_pick_stretch = polar_pos2[0]
    robot_pos2_pick_rotate = polar_pos2[1]
    robot_pos2_pick_height = polar_pos2[2]
    robot_pos2_drop_stretch = polar_pos2[3]
    robot_pos2_drop_rotate = polar_pos2[4]
    robot_pos2_drop_height = polar_pos2[5]

    robot_pos3_pick_stretch = polar_pos3[0]
    robot_pos3_pick_rotate = polar_pos3[1]
    robot_pos3_pick_height = polar_pos3[2]
    robot_pos3_drop_stretch = polar_pos3[3]
    robot_pos3_drop_rotate = polar_pos3[4]
    robot_pos3_drop_height = polar_pos3[5]

    default_stretch = polar_default[0]
    default_rotate = polar_default[1]
    default_height = polar_default[2]



    #in case every values are the same (after converting to and back from target system)
    if(correct):
        return True
    #in case values are not the same
    else:
        return False
