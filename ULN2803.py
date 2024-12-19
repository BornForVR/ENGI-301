#!/usr/bin/env python
import time
import os
import signal
import sys

# Motor is attached here
# P2_18/20/22/24/ is connected to IN 1/2/3/4 on the drive board
controller = ["47", "64", "46", "44"]
states = [[1,1,0,0], [0,1,1,0], [0,0,1,1], [1,0,0,1]]
curState = 0   # Current state
ms = 100       # Time between steps, in ms
max = 200      # Number of steps to turn before turning around

CW  =  1       # Clockwise
CCW = -1
pos =  0       # current position and direction
direction = CW
GPIOPATH="/sys/class/gpio"

def signal_handler(sig, frame):
    print('Got SIGINT, turning motor off')
    for i in range(len(controller)) :
        f = open(GPIOPATH+"/gpio"+controller[i]+"/value", "w")
        f.write('0')
        f.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Hit ^C to stop')

def move():
    global pos
    global direction
    global minStep
    global maxStep
    pos += direction
    print("pos: " + str(pos))
    # Switch directions if at end.
    if (pos >= max or pos <= ms) :
        direction *= -1
    rotate(direction)

# This is the general rotate
def rotate(direction) :
    global curState
    global states
	# print("rotate(%d)", direction);
    # Rotate the state according to the direction of rotation
    curState +=  direction
    if(curState >= len(states)) :
        curState = 0;
    elif(curState<0) :
        curState = len(states)-1
    updateState(states[curState])

# Write the current input state to the controller
def updateState(state) :
    global controller
    print(state)
    for i in range(len(controller)) :
        f = open(GPIOPATH+"/gpio"+controller[i]+"/value", "w")
        f.write(str(state[i]))
        f.close()

# Initialize motor control pins to be OUTPUTs
for i in range(len(controller)) :
    # Make sure pin is exported
    if (not os.path.exists(GPIOPATH+"/gpio"+controller[i])):
        f = open(GPIOPATH+"/export", "w")
        f.write(pin)
        f.close()
    # Make it an output pin
    f = open(GPIOPATH+"/gpio"+controller[i]+"/direction", "w")
    f.write("out")
    f.close()

# Put the motor into a known state
updateState(states[0])
rotate(direction)

# Rotate
while True:
    move()
    time.sleep(ms/1000)

