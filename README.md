# Diplomová práca
    Version control for DP

## What it includes?
  Flask webserver writen in python, with gevent-websocket. Website uses javscript,html and css. It allows to control
  
## Requirements
* ```python3.x.x```        -to run webserver
* ```pip3```               -to easily install other requirements
* ```flask```              -server 
* ```flask-socketio```     -socketio
* ```gevent```             -gevent websocket
* ```gevent-websocket```   -gevent websocket
* ```serial```             -for raspberry to comunicate with arduino
* ```colorama```           -color text output
* ```numpy```              -for conversion from/to polar coordinates

It is important to have this folder downloaded in same folder as ```uArm-Python-SDK```. Which can be downloaded here ```https://github.com/uArm-Developer/uArm-Python-SDK``` and follow steps to install properly.


## How to use
Install pip3 (run this in terminal ```sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py``` , then ``` sudo python3 get-pip.py```) after that instal flask (```sudo pip3 install flask```), flask_socketio (```sudo pip3 install flask_socketio```) and so on until you fulfill all requirements.

For easier use install python3.x.x and pip3 (python package installer) and run this command
```
sudo pip3 install -r requirements.txt 
```
