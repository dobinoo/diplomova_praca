from uarm.wrapper import SwiftAPI                   #uArm SwiftPro libraries
import sys
import os
import math
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../uArm-Python-SDK'))      #link to uArm SwiftPro python3.x.x library
swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready(timeout=5)

stretch = 200
rotation = 91


swift.set_polar(stretch=stretch,rotation=rotation,height=150,speed=100000)
time.sleep(2)
#swift.set_position(x=185.44555,y=74.92999,z=150,speed=100000)
print(swift.get_polar())
print(swift.get_position())


x = stretch * math.cos(math.radians(rotation-90))
y = stretch * math.sin(math.radians(rotation-90))


print("X: ",x)
print("Y: ",y)
time.sleep(5)

swift.set_position(x=x,y=y,z=150,speed=100000)


r = math.sqrt(pow(x,2) + pow(y,2))
phi = math.atan(y/x)
phi = math.degrees(phi) + 90

print("R",r)
print("Phi",phi)

time.sleep(5)

swift.set_polar(stretch=r,rotation=phi,height=150,speed=100000)
#
# for i in list(range(6)):
#     print(i)
# time.sleep(3)

#swift.set_polar(stretch = r, rotation=phi, height=150, speed=100000 )

# result = test()
# print(pos1[1])
# print(type(result[0]))
# print("\n")
# print(type(result[1]))
# print(r)
# print("\n")
# print(phi)
# print("\n")
#
# print(round(phi))
