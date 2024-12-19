import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP0
import time
from LCD import LCD
import os

# Motor GPIO configuration
controller = ["47", "64", "46", "44"]  # GPIO numbers for the motor
states = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]  # Stepping states
curState = 0  # Current stepping state index
steps_per_degree = (512 * 4) / 360  # Steps needed for one degree rotation

# Rotary encoder setup
encoder = RotaryEncoder(eQEP0)
encoder.setAbsolute()
encoder.enable()

# LCD Display setup
lcd = LCD(1, 0x27, True)  # Setup LCD display

# Initialize GPIO for motor
GPIOPATH = "/sys/class/gpio"
for pin in controller:
    if not os.path.exists(GPIOPATH + "/gpio" + pin):
        with open(GPIOPATH + "/export", "w") as f:
            f.write(pin)
    with open(GPIOPATH + "/gpio" + pin + "/direction", "w") as f:
        f.write("out")

def updateState(state):
    """ Write the current state to the motor pins """
    for i, pin_state in enumerate(state):
        with open(GPIOPATH + "/gpio" + controller[i] + "/value", "w") as f:
            f.write(str(pin_state))

def rotate_motor(steps):
    """ Rotate the motor by the specified number of steps """
    global curState
    for _ in range(abs(steps)):
        curState = (curState + (1 if steps > 0 else -1)) % len(states)
        updateState(states[curState])
        time.sleep(0.01)  # Control speed of rotation

# Main program
last_angle = None
try:
    while True:
        # Read the current position from the rotary encoder
        current_angle = encoder.position
        # Calculate change in angle
        if last_angle is not None:
            angle_change = current_angle - last_angle
            # Convert angle change to step count
            step_count = int(angle_change * steps_per_degree)
            # Rotate motor based on the change in angle
            rotate_motor(step_count)
        
        # Update the display only if the angle has changed
        if current_angle != last_angle:
            lcd.clear()
            lcd.message(f'Angle: {current_angle}')
            last_angle = current_angle
        
        time.sleep(0.1)  # Debounce interval

except KeyboardInterrupt:
    print("Program stopped by User")
finally:
    GPIO.cleanup()
    lcd.clear()
    encoder.disable()

