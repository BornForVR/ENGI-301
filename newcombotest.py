import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP0
import time
from LCD import LCD
import os

# Motor GPIO configuration
controller1 = ["47", "64", "46", "44"]  # GPIO numbers for the first motor
controller2 = ["58", "57", "60", "52"]  # GPIO numbers for the second motor
states = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]  # Stepping states
curState = 0  # Current stepping state index
steps_per_degree = (512 * 4) / 360  # Steps needed for one degree rotation
scale_factor = 5  # Scale factor for steps

# Rotary encoder setup
encoder = RotaryEncoder(eQEP0)
encoder.setAbsolute()
encoder.enable()

# LCD Display setup
lcd = LCD(1, 0x27, True)  # Setup LCD display

# Setup the button
button_pin = 'P2_32'  # Define the GPIO pin for the button
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize GPIO for both motors
GPIOPATH = "/sys/class/gpio"
all_controllers = controller1 + controller2  # Combine both motor controllers
for pin in all_controllers:
    if not os.path.exists(GPIOPATH + "/gpio" + pin):
        with open(GPIOPATH + "/export", "w") as f:
            f.write(pin)
    with open(GPIOPATH + "/gpio" + pin + "/direction", "w") as f:
        f.write("out")

def update_motors(state1, state2):
    """ Write the current state to the motor pins for both motors """
    for i in range(len(controller1)):
        with open(GPIOPATH + "/gpio" + controller1[i] + "/value", "w") as f1:
            f1.write(str(state1[i]))
        with open(GPIOPATH + "/gpio" + controller2[i] + "/value", "w") as f2:
            f2.write(str(state2[i]))

def rotate_motors(steps):
    """ Rotate the motors by the specified number of steps """
    global curState
    for _ in range(abs(steps)):
        # Adjust curState and calculate the next state for each motor
        curState = (curState + (1 if steps > 0 else -1)) % len(states)
        motor1_state = states[curState]  # Normal direction
        motor2_state = states[len(states) - 1 - curState]  # Reversed direction
        # Update both motors in the same function call
        update_motors(motor1_state, motor2_state)
        time.sleep(0.001)  # Control the speed of rotation


def reset_motor_position():
    """ Resets both motors to the initial position (0 degrees) """
    current_angle = encoder.position
    # Calculate the number of steps needed to return to the original position
    steps_to_initial = -int(current_angle * steps_per_degree * scale_factor)
    # Use the single function call to reset both motors
    rotate_motors(steps_to_initial)
    # Reset the encoder position to synchronize it with the physical motor positions
    encoder.position = 0
    # Update the LCD display to show the reset position
    lcd.clear()
    lcd.message('Angle: 0')
    print("Motors reset to initial position.")

# Main program loop
last_angle = None
try:
    while True:
        # Read the current position from the rotary encoder
        current_angle = encoder.position
        
        # Handle button press for resetting motors
        if not GPIO.input(button_pin):
            reset_motor_position()  # Call the reset function to reset motor positions
            last_angle = 0 
            continue 


        # Calculate change in angle
        if last_angle is not None:
            angle_change = current_angle - last_angle
            step_count = int(angle_change * steps_per_degree * scale_factor)
            rotate_motors(step_count)
        
        # Update the display only if the angle has changed
        if current_angle != last_angle:
            lcd.clear()
            lcd.message(f'Angle: {current_angle}')
            last_angle = current_angle
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by User")
finally:
    GPIO.cleanup()
    lcd.clear()
    encoder.disable()