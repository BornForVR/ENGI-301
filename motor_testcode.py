#!/usr/bin/env python
import time
import os
import signal
import sys

# Configuration for motor GPIOs
controller = ["47", "64", "46", "44"]  # Define GPIO numbers
#controller = ["58", "57", "60", "52"]  # Define GPIO numbers
states = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
curState = 0  # Current state index
ms = 1       # Time between steps, in ms
steps_for_360_degrees = 512*4  # Calculated steps to achieve 360 degrees

# Motor control setup
direction = 1  # CW (1) or CCW (-1), set as needed
GPIOPATH = "/sys/class/gpio"

def signal_handler(sig, frame):
    print('Got SIGINT, turning motor off')
    for i in range(len(controller)):
        with open(GPIOPATH + "/gpio" + controller[i] + "/value", "w") as f:
            f.write('0')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Hit ^C to stop')

def rotate(steps):
    global curState
    for _ in range(steps):
        curState = (curState + direction) % len(states)
        updateState(states[curState])
        time.sleep(ms / 1000.0)

def updateState(state):
    for i, pin_state in enumerate(state):
        with open(GPIOPATH + "/gpio" + controller[i] + "/value", "w") as f:
            f.write(str(pin_state))

# Initialize GPIOs for motor control
for pin in controller:
    if not os.path.exists(GPIOPATH + "/gpio" + pin):
        with open(GPIOPATH + "/export", "w") as f:
            f.write(pin)
    with open(GPIOPATH + "/gpio" + pin + "/direction", "w") as f:
        f.write("out")

# Initial motor state setup
updateState(states[0])

# Execute rotation
rotate(steps_for_360_degrees)
