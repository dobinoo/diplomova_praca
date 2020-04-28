from flask import Flask, render_template, url_for   #server libraries
from flask_socketio import SocketIO, emit           #flask socket libraries
from uarm.wrapper import SwiftAPI                   #uArm SwiftPro libraries
from colorama import Fore, Style                    #color text libraries
import serial                                       #arduino connection library
import sys                                          #system library
import os                                           #os library
import time                                         #time library
import csv                                          #coma separated values library
#import robot_moving

print("\033c", end="")
print("Connect to webserver\n")
time.sleep(2)
print("Preparing Arduino and uArm SwiftPro please wait\n")
#test_a = True
#test_b = True

#arduino positions (can be change for specific requirement)
arduino_pos1 = 28
arduino_pos2 = 75
arduino_pos3 = 116


arduino_max = 135

#Robot position globals
#pos1
robot_pos1_stretch = 207
robot_pos1_rotate = 88
robot_pos1_height = 40

#pos2
robot_pos2_stretch = 200
robot_pos2_rotate = 91
robot_pos2_height = 37

#pos3
robot_pos3_stretch = 215
robot_pos3_rotate = 88
robot_pos3_height = 37

#default change to give position_data

robot_change_height = 90
# robot_change_stretch
# robot_change_rotation
########################


#setting up flask server
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

arduino_actual_position = 0

##############################arduino functions########################
def arduino_send(number, direction):
    global name
    global ser

    #ser = serial.Serial('/dev/ttyUSB0',115200,timeout=2);     #serial name for arduino getting it from global (from initialization)
    #ser.open()
    #print(ser.name)
    #ser.flush()                                     #flushing serial

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
    arduino.arduino_send(0,"R")                          #for resetting values in arduino (in case of server reset and not arduino)
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
    swift.set_polar(stretch=151,rotation=90,height=80,speed=100000)
    time.sleep(3)
    return

#set robot to certain position
def robot_position(stretch, rotation ,height):
    global swift
    swift.set_polar(stretch=stretch,rotation=rotation,height=height,speed=100000)
    print(stretch)
    print(rotation)
    print(height)
    time.sleep(3)
    return

#taking and grabing
def robot_take(pos):
    global swift
    global robot_pos1_stretch,robot_pos1_rotate, robot_pos1_height
    global robot_pos2_stretch,robot_pos2_rotate, robot_pos2_height
    global robot_pos3_stretch,robot_pos3_rotate, robot_pos3_height
    global robot_change_height


    if(pos == 1):
        swift.set_polar(stretch=robot_pos1_stretch,rotation=robot_pos1_rotate,height=robot_pos1_height,speed=100000)  #take position
        #robot_position(robot_pos1_stretch,robot_pos1_rotate, robot_pos1_height)
        robot_waiting()
        swift.set_gripper(catch=True)                                   #catch ball
        time.sleep(3)
        swift.set_polar(stretch=robot_pos1_stretch-54,rotation=robot_pos1_rotate,height=robot_pos1_height + 10,speed=100000)  #take position
        robot_waiting()
        swift.set_polar(stretch=robot_pos1_stretch-54,rotation=robot_pos1_rotate,height=142,speed=100000)  #give position
        robot_waiting()
        swift.set_polar(stretch=robot_pos1_stretch,rotation=robot_pos1_rotate,height=142,speed=100000)  #give position
        robot_waiting()
        swift.set_polar(stretch=robot_pos1_stretch,rotation=robot_pos1_rotate,height=robot_pos1_height + robot_change_height + 1,speed=6000)  #give position
        robot_waiting()
        swift.set_gripper(catch=False)                                  #let ball
        time.sleep(3)
        swift.set_polar(stretch=robot_pos1_stretch-54,rotation=robot_pos1_rotate,height=140,speed=100000)  #give position #give position
        robot_waiting()
        default_robot_position()

    if(pos == 2):
        swift.set_polar(stretch=robot_pos2_stretch,rotation=robot_pos2_rotate,height=robot_pos2_height,speed=100000)  #take position
        #robot_position(robot_pos2_stretch,robot_pos2_rotate, robot_pos2_height)
        robot_waiting()
        swift.set_gripper(catch=True)                                   #catch ball
        time.sleep(3)
        swift.set_polar(stretch=robot_pos2_stretch-42,rotation=robot_pos2_rotate,height=robot_pos2_height + 10,speed=100000)  #take position
        robot_waiting()
        swift.set_polar(stretch=robot_pos2_stretch-42,rotation=robot_pos2_rotate,height=142,speed=100000)  #give position
        robot_waiting()
        swift.set_polar(stretch=robot_pos2_stretch,rotation=robot_pos2_rotate,height=142,speed=100000)  #give position
        robot_waiting()
        swift.set_polar(stretch=robot_pos2_stretch,rotation=robot_pos2_rotate,height=robot_pos2_height + robot_change_height + 1,speed=6000)  #give position
        robot_waiting()
        swift.set_gripper(catch=False)                                  #let ball
        time.sleep(3)
        swift.set_polar(stretch=robot_pos2_stretch-42,rotation=robot_pos2_rotate,height=140,speed=100000)  #give position #give position
        robot_waiting()
        default_robot_position()


    if(pos == 3):
        swift.set_polar(stretch=robot_pos3_stretch,rotation=robot_pos3_rotate,height=robot_pos3_height,speed=100000)  #take position
        #robot_position(robot_pos3_stretch,robot_pos3_rotate, robot_pos3_height)
        robot_waiting()
        swift.set_gripper(catch=True)                                   #catch ball
        time.sleep(3)
        swift.set_polar(stretch=robot_pos3_stretch-62,rotation=robot_pos3_rotate,height=robot_pos3_height + 10,speed=100000)  #take position
        robot_waiting()
        swift.set_polar(stretch=robot_pos3_stretch-62,rotation=robot_pos3_rotate,height=142,speed=100000)  #give position
        robot_waiting()
        swift.set_polar(stretch=robot_pos3_stretch,rotation=robot_pos3_rotate,height=142,speed=100000)  #give position
        robot_waiting()
        swift.set_polar(stretch=robot_pos3_stretch,rotation=robot_pos3_rotate,height=robot_pos3_height + robot_change_height+1,speed=6000)  #give position
        robot_waiting()
        swift.set_gripper(catch=False)                                  #let ball
        time.sleep(3)
        swift.set_polar(stretch=robot_pos3_stretch-62,rotation=robot_pos3_rotate,height=142,speed=100000)  #give position #give position
        robot_waiting()
        default_robot_position()

    return

#robot waiting time
def robot_waiting():
    time.sleep(1)
    return
########################TODO TODO TODO TODO TODO##############################33
#########################################TODO TODO TODO TODO TODO##############

#unpause function
def unpause_function():
    emit('unpause')
    print("Unpausing buttons")
    return

#Experiment A
@socketio.on('a_place', namespace='/test')
def ExprimentA(message):
    global arduino_pos1
    print("Moving")
    arduino_shortest_way(arduino_pos1)  #send arduino to experiment A with pos1
    robot_take(1)
    print("A")
    unpause_function()

#Experiment B
@socketio.on('b_place', namespace='/test')
def ExprimentB(message):
    global arduino_pos2
    print("Moving")
    arduino_shortest_way(arduino_pos2)  #send arduino to experiment B with pos2
    robot_take(2)
    print("B")
    unpause_function()

#Experiment C
@socketio.on('c_place', namespace='/test')
def ExprimentC(message):
    #global arduino_actual_position
    global arduino_pos3
    print("Moving")
    arduino_shortest_way(arduino_pos3)  #send arduino to experiment B with pos3
    robot_take(3)
    print("C")
    unpause_function()

#button distance onclick
@socketio.on('distance', namespace='/test')
def DistanceMoving(direction,number):
    global arduino_actual_position

    # arduino.arduino_move(int(number),str(direction))
    arduino_move(int(number),str(direction))
    arduino_position_update(int(number),direction)
    time.sleep(arduino_sleep(int(number)))
    unpause_function()
    print("direction: ",direction)
    print("distance",number)

#button robot position onclick
@socketio.on('position', namespace='/test')
def RobotPosition(array):
    global swift
    height = array[0]
    stretch = array[1]
    rotate = array[2]

    robot_position(int(stretch),int(rotate),int(height)) #setting specific position
    robot_waiting()
    #swift.set_polar(stretch=stretch,rotation=rotate,height=height,speed=100000)
    #robot_moving.move(stretch,rotate,height)
    unpause_function()
    print(height)
    print(stretch)
    print(rotate)

#default path (what server loads on start)
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


#initializing connections between raspberry and arduino/uArm
@app.before_first_request       #must do in function under this annotation otherwise restart 2 times and causing error
def initialize():
    test_a = True
    test_b = True

    try:
        global serial_name
        global ser

        #serial_name = input("Please enter arduino port: ")
        #serial_name = "/dev/" + serial_name
        #ser.flush()
        #print(ser.name)
        #arduino_reset()

        ser = serial.Serial('/dev/ttyUSB0',115200,timeout=2)        #arduino serial
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


#starting server
if __name__ == "__main__":
    try:
        #app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
        socketio.run(app, host='0.0.0.0', port=80, debug=True, use_reloader=False)          #starting app , 0.0.0.0 (on device local ip adress, eg 192.168.0.112) , on port 80, with debug and no reloader (restart server after changes)
        #socketio.run(app, host='0.0.0.0', port=80, debug=True)
    except:
        print(Fore.RED + "ERROR STARTING SERVER")
