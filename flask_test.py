from flask import Flask, render_template, url_for   #server libraries
from threading import Lock
from flask_socketio import SocketIO, emit           #flask socket libraries
from uarm.wrapper import SwiftAPI                   #uArm SwiftPro libraries
from colorama import Fore, Style                    #color text libraries
import serial                                       #arduino connection library
import sys                                          #system library
import os                                           #os library
import time                                         #time library
#import csv                                         #coma separated values library (intendet to create file log) not used
from conversions import *                           #file responsible for converting from different coordinate system

print("\033c", end="")                      #clears command line

#informative text
print("Connect to webserver\n")
time.sleep(2)
print("Preparing Arduino and uArm SwiftPro please wait\n")


#arduino positions (can be change for specific requirement)
arduino_pos1 = 28
arduino_pos2 = 75
arduino_pos3 = 116
arduino_actual_position = 0         #arduino start position
arduino_max = 135                   #arduino maximal position


#######################Robot cartesian coordinates#############################
#if true then coordinates are in cartesian system(must be set false to use default values - robot_pos1_pick_stretch, robot_pos1_pick_height ....)
cartesian = False

#default uArm position
default_x = 151
default_y = 90
default_z = 80

###############Position1#####################
#robot pos1 pick
robot_pos1_pick_x = 207
robot_pos1_pick_y = 88
robot_pos1_pick_z = 40

#robot pos1 drop
robot_pos1_drop_x = 207
robot_pos1_drop_y = 88
robot_pos1_drop_z = 131
##############################################

################Position2#####################
#robot pos2 pick
robot_pos2_pick_x = 200
robot_pos2_pick_y = 91
robot_pos2_pick_z = 37

#robot pos2 drop
robot_pos2_drop_x = 200
robot_pos2_drop_y = 91
robot_pos2_drop_z = 128
###############################################

################Position3#####################
#robot pos3 pick
robot_pos3_pick_x = 215
robot_pos3_pick_y = 90
robot_pos3_pick_z = 37

#robot pos3 drop
robot_pos3_drop_x = 215
robot_pos3_drop_y = 90
robot_pos3_drop_z = 128
###############################################
#######################Robot cartesian coordinates#############################

#######################Robot polar coordinates#############################
#default uArm position
default_stretch = 151
default_rotation = 90
default_height = 80

###############Position1#####################
#robot pos1 pick
robot_pos1_pick_stretch = 207
robot_pos1_pick_rotate = 88
robot_pos1_pick_height = 40

#robot pos1 drop
robot_pos1_drop_stretch = 207
robot_pos1_drop_rotate = 88
robot_pos1_drop_height = 131
##############################################

################Position2#####################
#robot pos2 pick
robot_pos2_pick_stretch = 200
robot_pos2_pick_rotate = 91
robot_pos2_pick_height = 37

#robot pos2 drop
robot_pos2_drop_stretch = 200
robot_pos2_drop_rotate = 91
robot_pos2_drop_height = 128
###############################################

################Position3#####################
#robot pos3 pick
robot_pos3_pick_stretch = 215
robot_pos3_pick_rotate = 90
robot_pos3_pick_height = 37

#robot pos3 drop
robot_pos3_drop_stretch = 215
robot_pos3_drop_rotate = 90
robot_pos3_drop_height = 128
###############################################
#######################Robot polar coordinates#############################

#default change to give position_data (changed for specific position) - obsolete
#robot_change_height = 90
# robot_change_stretch
# robot_change_rotation
########################


#setting up flask server
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

##############################arduino functions########################
def arduino_send(number, direction):
    global name
    global ser

    #checking if arduino is reseting
    if(direction == "R"):
        message = "000RE"
        print(Fore.BLUE + "Resetting arduino\n")
        print(Style.RESET_ALL)
    else:
        print(Fore.BLUE + "Converting to bytes:\n")
        print(Style.RESET_ALL)

        #fixing number
        if number < 10:
            updated_number = "00" + str(number)

        if number < 100:
            if number >= 10:
                updated_number = "0" + str(number)

        if number >= 100:
            updated_number = str(number)
        ##############

        message = updated_number + direction + "E"     #E is ending character for arduino
        print(message)

    try:
        ser.write(message.encode())                    #converting and sending to arduino
    except:
        print(Fore.RED + "Cant send data to arduino -- arduino.py\n")
        print(Style.RESET_ALL)

    return

#function to arduino to move
def arduino_move(number_input, direction):
    global arduino_actual_position
    actual_distance = arduino_actual_position
    max_distance = 135
    number = int(number_input)

    #direction checking
    if direction == "F":
        if actual_distance + number<= 135:
            actual_distance = actual_distance + number
            arduino_send(number, direction)
            print("\nIt will now move " + str(number_input) + "cm" + " forward\n")
        else:
            print(Fore.RED + "Cant move that direction, current position: ",actual_distance)
            print(Style.RESET_ALL + "\n\n")

    elif direction == "B":
        if actual_distance - number >= 0:
            actual_distance = actual_distance - number
            arduino_send(number, direction)
            print("It will now move " + str(number_input) + "cm" + " backward\n")
        else:
            print(Fore.RED  + "Cant move that direction, current position: ",actual_distance)
            print(Style.RESET_ALL + "\n\n")
    return


#how long wait and pause buttons for arduino
def arduino_sleep(travel_distance):
    wait_time = int(travel_distance / 7) + 1        #7 is 7cm per 1s
    return wait_time

def arduino_reset():
    arduino_send(0,"R")                          #for resetting values in arduino (in case of server reset and not arduino)
    return

#shortest way from experiment to experiment
def arduino_shortest_way(arduino_pos):
    global arduino_actual_position

    if(arduino_pos-arduino_actual_position>0):
        arduino_move(int(arduino_pos-arduino_actual_position),"F")
        print("Sleeping for: ",int(arduino_pos-arduino_actual_position))
        sleep = int(arduino_pos-arduino_actual_position)
        time.sleep(arduino_sleep(sleep))
        arduino_position_update(arduino_pos-arduino_actual_position,"F")


    if(arduino_actual_position - arduino_pos>0):
        arduino_move(int(arduino_actual_position - arduino_pos),"B")
        print("Sleeping for: ",int(arduino_actual_position - arduino_pos))
        sleep = int(arduino_actual_position - arduino_pos)
        time.sleep(arduino_sleep(sleep))
        arduino_position_update(arduino_actual_position - arduino_pos,"B")

    return

#writing changes for actual arduino positions
def arduino_position_update(change,direction):
    global arduino_actual_position
    print("Arduino old position: ",arduino_actual_position)

    if(direction == "F"):
        if(change + arduino_actual_position <= 135):
            arduino_actual_position = change + arduino_actual_position
    if(direction == "B"):
        if(arduino_actual_position - change >= 0):
            arduino_actual_position =arduino_actual_position -  change

    print("Arduino new position: ",arduino_actual_position)
    return arduino_actual_position

#########################################################################

###################################robot functions TODO TODO TODO TODO TODO##############################
#default robot position to not collide#
def default_robot_position():
    global swift
    global default_stretch
    global default_rotation
    global default_height

    swift.set_polar(stretch=default_stretch,rotation=default_rotation,height=default_height,speed=100000)
    time.sleep(2)
    return

#set robot to certain position
def robot_position(stretch, rotation ,height,speed):
    global swift
    swift.set_polar(stretch=stretch,rotation=rotation,height=height,speed=speed)
    robot_waiting()

    #debug outputs
    #print(stretch)
    #print(rotation)
    #print(height)

    return

def robot_gripper(catch):
    swift.set_gripper(catch=catch)
    time.sleep(3)
    return

#taking and grabing
def robot_take(pos):

    #position 1
    global robot_pos1_pick_stretch,robot_pos1_pick_rotate, robot_pos1_pick_height
    global robot_pos1_drop_stretch,robot_pos1_drop_rotate, robot_pos1_drop_height

    #position 2
    global robot_pos2_pick_stretch,robot_pos2_pick_rotate, robot_pos2_pick_height
    global robot_pos2_drop_stretch,robot_pos2_drop_rotate, robot_pos2_drop_height

    #position 3
    global robot_pos3_pick_stretch,robot_pos3_pick_rotate, robot_pos3_pick_height
    global robot_pos3_drop_stretch,robot_pos3_drop_rotate, robot_pos3_drop_height

    speed = 100000

    if(pos == 1):
        robot_position(robot_pos1_pick_stretch,robot_pos1_pick_rotate, robot_pos1_pick_height,speed)            #pick up ball position
        robot_gripper(True)                                                                                     #pick up ball
        default_robot_position()                                                                                #default pos
        robot_position(default_stretch,robot_pos1_pick_rotate,robot_pos1_drop_height + 5,speed)                 #go up to drop height
        robot_position(robot_pos1_drop_stretch,robot_pos1_drop_rotate, robot_pos1_drop_height + 5,speed)        #stretch to drop position
        robot_position(robot_pos1_drop_stretch,robot_pos1_drop_rotate, robot_pos1_drop_height,6000)             #lower to drop position
        robot_gripper(False)                                                                                    #drop ball
        robot_position(default_stretch,robot_pos1_pick_rotate,robot_pos1_drop_height + 5,speed)                 #go to default stretch
        default_robot_position()                                                                                #default position

    if(pos == 2):
        robot_position(robot_pos2_pick_stretch,robot_pos2_pick_rotate, robot_pos2_pick_height,speed)            #pick up ball position
        robot_gripper(True)                                                                                     #pick up ball
        default_robot_position()                                                                                #default pos
        robot_position(default_stretch,robot_pos2_pick_rotate,robot_pos2_drop_height + 5,speed)                 #go up to drop height
        robot_position(robot_pos2_drop_stretch,robot_pos2_drop_rotate, robot_pos2_drop_height + 5,speed)        #stretch to drop position
        robot_position(robot_pos2_drop_stretch,robot_pos2_drop_rotate, robot_pos2_drop_height,6000)             #lower to drop position
        robot_gripper(False)                                                                                    #drop ball
        robot_position(default_stretch,robot_pos2_pick_rotate,robot_pos2_drop_height + 5,speed)                 #go to default stretch
        default_robot_position()                                                                                #default position

    if(pos == 3):
        robot_position(robot_pos3_pick_stretch,robot_pos3_pick_rotate, robot_pos3_pick_height,speed)            #pick up ball position
        robot_gripper(True)                                                                                     #pick up ball
        default_robot_position()                                                                                #default pos
        robot_position(default_stretch,robot_pos3_pick_rotate,robot_pos3_drop_height + 5,speed)                 #go up to drop height
        robot_position(robot_pos3_drop_stretch,robot_pos3_drop_rotate, robot_pos3_drop_height + 5,speed)        #stretch to drop position
        robot_position(robot_pos3_drop_stretch,robot_pos3_drop_rotate, robot_pos3_drop_height,6000)             #lower to drop position
        robot_gripper(False)                                                                                    #drop ball
        robot_position(default_stretch,robot_pos3_pick_rotate,robot_pos3_drop_height + 5,speed)                 #go to default stretch
        default_robot_position()                                                                                #default position

    return

#robot waiting time
def robot_waiting():
    time.sleep(1)
    return


#unpause function
def unpause_function():
    emit('unpause')
    print("Unpausing buttons")
    return


#Experiment A
@socketio.on('a_place', namespace='/test')
def ExprimentA():
    global arduino_pos1
    print("Moving")
    arduino_shortest_way(arduino_pos1)  #send arduino to experiment A with pos1
    robot_take(1)
    print("A")
    unpause_function()
    return

#Experiment B
@socketio.on('b_place', namespace='/test')
def ExprimentB():
    global arduino_pos2
    print("Moving")
    arduino_shortest_way(arduino_pos2)  #send arduino to experiment B with pos2
    robot_take(2)
    print("B")
    unpause_function()
    return

#Experiment C
@socketio.on('c_place', namespace='/test')
def ExprimentC():
    global arduino_pos3
    print("Moving")
    arduino_shortest_way(arduino_pos3)  #send arduino to experiment B with pos3
    robot_take(3)
    print("C")
    unpause_function()
    return


#button distance onclick
@socketio.on('distance', namespace='/test')
def DistanceMoving(direction,number):
    global arduino_actual_position

    arduino_move(int(number),str(direction))
    arduino_position_update(int(number),direction)
    time.sleep(arduino_sleep(int(number)))
    unpause_function()
    print("direction: ",direction)
    print("distance",number)
    return

@socketio.on('default_pos', namespace='/test')
def DefaultPosition():
    default_robot_position()
    print("Going default position\n")
    unpause_function()
    return


#button robot position onclick
@socketio.on('position', namespace='/test')
def RobotPosition(array):
    global swift
    speed = 100000
    height = array[0]
    stretch = array[1]
    rotate = array[2]

    robot_position(int(stretch),int(rotate),int(height),speed) #setting specific position
    robot_waiting()
    unpause_function()

    #debug outputs
    # print(height)
    # print(stretch)
    # print(rotate)
    return

#default path (what server loads on start)
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


#initializing connections between raspberry and arduino/uArm
@app.before_first_request       #initialization of uArm and arduino must be in the function under this annotation otherwise server restarts few times and causing error
def initialize():
    global cartesian
    test_a = True
    test_b = True

    #convert cartesian coordinates to polar coordinates
    if(cartesian):
        print(Fore.BLUE + "Detecting cartesian coordinates, changing to polar")

        #test to check converting cartesian to polar
        if(test_converting(cartesian)):
            print(Fore.GREEN + "TEST OK")
            print(Style.RESET_ALL)
        else:
            print(Fore.RED + "TEST FAILED")
            print(Style.RESET_ALL)

        #debug outputs
        # print(default_stretch)
        # print(default_rotation)
        # print(default_height)

        change_variables_to_polar()
        print(Fore.GREEN + "Conversion from cartesian to polar successfull")
        print(Style.RESET_ALL)
        time.sleep(2)
    else:
        print(Fore.BLUE + "Default polar coordinates are set")
        print(Style.RESET_ALL)



    try:
        global serial_name
        global ser

        ser = serial.Serial('/dev/ttyUSB0',115200,timeout=2)        #arduino serial
        arduino_reset()
        print(Fore.BLUE + "Arduino UNO\n")
    except:
        test_a = False
        print(Fore.RED + "FAILED CONNECT TO ARDUINO!")
        print(Style.RESET_ALL)


    #setting up uArm SwiftPro
    try:
        global swift
        #need to change
        sys.path.append(os.path.join(os.path.dirname(__file__), '../uArm-Python-SDK'))      #link to uArm SwiftPro python3.x.x library
        swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
        swift.waiting_ready(timeout=5)
        swift.set_mode(0)
        device_info = swift.get_device_info()
        default_robot_position()
        print(Fore.BLUE)
        print(device_info)
        print("\n")
    except:
        test_b = False
        print(Fore.RED + "FAILED CONNECT TO uArm SwiftPro")
        print(Style.RESET_ALL)

    if test_a and test_b:
        print(Fore.GREEN + "DONE!\n")

    print(Style.RESET_ALL)
    return

#starting server
if __name__ == "__main__":
    try:
        #app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
        socketio.run(app, host='0.0.0.0', port=80, debug=True)          #starting app , 0.0.0.0 (on device local ip adress, eg 192.168.0.112) , on port 80, with debug and no reloader (restart server after changes)
        #socketio.run(app, host='0.0.0.0', port=80, debug=True)
    except:
        print(Fore.RED + "ERROR STARTING SERVER")
