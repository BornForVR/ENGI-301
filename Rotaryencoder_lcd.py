import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP0
import time
from LCD import LCD

# Set up the pin for the switch
switch_pin = 'P2_32'
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up the rotary encoder on eQEP0
myEncoder = RotaryEncoder(eQEP0)
myEncoder.setAbsolute()
myEncoder.enable()

# Initialize the LCD display
lcd = LCD(1, 0x27, True)  # Adjust the I2C bus and address as needed

# Helper variables to track the last state
last_switch_state = GPIO.HIGH
last_angle = None  # Initialize last_angle to track changes in encoder position

try:
    while True:
        # Read the state of the switch
        current_switch_state = GPIO.input(switch_pin)
        
        # Check for button press (transition from HIGH to LOW)
        if last_switch_state == GPIO.HIGH and current_switch_state == GPIO.LOW:
            # Reset the encoder position when button is pressed
            myEncoder.position = 0
            angle = myEncoder.position  # Update angle to the reset position
            lcd.clear()  # Clear the display when resetting the position
            lcd.message(f'Angle: {angle}')  # Display the new (reset) angle
            print("Angle reset to:", angle)  # Output to console for debugging

        # Update the last switch state
        last_switch_state = current_switch_state

        # Get the current position of the encoder
        angle = myEncoder.position
        
        # Update the display only if the angle has changed
        if angle != last_angle:
            lcd.clear()  # Clear the display to update the angle
            lcd.message(f'Angle: {angle}')  # Display the angle value dynamically
            last_angle = angle  # Update last_angle to the current angle
            print("Angle:", angle)  # Also output to console
        
        time.sleep(0.1)  # Polling interval to debounce the switch
except KeyboardInterrupt:
    print("Program stopped by User")
finally:
    GPIO.cleanup()  # Clean up GPIO to ensure all pins are reset
    lcd.clear()  # Clear the LCD display
    myEncoder.disable()  # Disable the encoder



