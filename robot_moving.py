import os
import sys
import time
from uarm.wrapper import SwiftAPI




def move(stretch, rotate, height):
    global swift
    swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
    swift.set_mode(0)
    swift.set_polar(stretch=stretch,rotation=rotate,height=height,speed=100000)
    return

def catch(catch):
    global swift

    swift.set_gripper(catch=catch)
    return
#move()
