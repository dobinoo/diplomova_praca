import serial
import os
import sys
from colorama import Fore, Style
from time import sleep
from flask_test import arduino_actual_position


actual_distance = arduino_actual_position

#moving number checking
def arduino_send(number, direction):
    global name
    ser = serial.Serial('/dev/ttyUSB0',115200,timeout=2);     #serial name for arduino
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
    global actual_distance
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
