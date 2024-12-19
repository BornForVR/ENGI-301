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
    
def rotate_motors(total_steps):
    """ Rotate the motors by the specified number of steps with the ability to stop mid-way """
    global curState
    step_increment = 10  # Number of steps to move before checking the button state
    steps_processed = 0

    while steps_processed < abs(total_steps):
        if not GPIO.input(button_pin):  # Check if stop button is pressed
            stop_motors()
            return  # Exit the function early

        # Calculate the number of steps to take this iteration
        steps_this_iteration = min(step_increment, abs(total_steps) - steps_processed)
        direction = 1 if total_steps > 0 else -1

        # Execute the steps
        for _ in range(steps_this_iteration):
            curState = (curState + direction) % len(states)
            motor1_state = states[curState]  # Normal direction
            motor2_state = states[len(states) - 1 - curState]  # Reversed direction
            update_motors(motor1_state, motor2_state)
            time.sleep(0.0005)  # Control the speed of rotation

        steps_processed += steps_this_iteration

def stop_motors():
    """ Stops both motors and displays Stop message on LCD """
    lcd.clear()
    lcd.message('Stop!')
    for pin in controller1 + controller2:
        with open(GPIOPATH + "/gpio" + pin + "/value", "w") as f:
            f.write('0')
    print("Motors stopped.")

    
    
    
last_angle = None
try:
    while True:
        current_angle = encoder.position

        # Check if the button is pressed
        if not GPIO.input(button_pin):
            stop_motors()  # Stop all motor activity and show stop message
            last_angle = current_angle  # Update last_angle to current to prevent further movement
            continue

        # Calculate and apply motor rotation
        if last_angle is not None and current_angle != last_angle:
            angle_change = current_angle - last_angle
            if angle_change != 0:
                lcd.clear()
                # Check direction of the angle change
                if angle_change > 0:
                    lcd.message('Squeezing', 1)
                    lcd.message('Toothpaste!', 2)
                else:
                    lcd.message('Releasing')
                
                step_count = int(angle_change * steps_per_degree * scale_factor)
                rotate_motors(step_count)
            last_angle = current_angle
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by User")
finally:
    GPIO.cleanup()
    lcd.clear()
    encoder.disable()