# ENGI301
Repository for ENGI301 course work

## Project-1
This project focuses on building a toothpaste squeezer using a PocketBeagle board. The Cloud9 IDE is used for writing and testing all the code.

### Hardware and Components
Most of the parts are sourced from Inland at MicroCenter. The following components were used:

- **Rotary Encoder:**  
  - [Inland Rotary Encoder Module](https://community.microcenter.com/kb/articles/640-inland-rotary-encoder-module)  
  - [Shop Link](https://www.microcenter.com/product/618904/inland-ks0013-keystudio-rotary-encoder-module)

- **Stepper Motor (28BYJ-48) with ULN2003A Driver Board:**  
  - [Inland Stepper Motor Drive Board](https://community.microcenter.com/kb/articles/675-inland-stepper-motor-drive-board-5v-stepper-motor-3pcs)  
  - [Shop Link](https://www.microcenter.com/product/639726/inland-ks0327-keyestudio-stepper-motor-drive-board-5v-stepper-motor-kit-(3pcs))

- **1602 I2C LCD Display Module:**  
  - [Inland 1602 I2C Module](https://community.microcenter.com/kb/articles/649-inland-1602-i2c-module)  
  - [Shop Link](https://www.microcenter.com/product/632704/inland-1602-i2c-lcd-display-module)

### Code Files in this Repository
- [LCD.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/LCD.py)
- [lcd_test.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/lcd_test.py)
- [rotaryEncoder.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/rotaryEncoder.py)
- [Rotaryencoder_lcd.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Rotaryencoder_lcd.py)
- [motor_testcode.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/motor_testcode.py)
- [combo_test_code.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/combo_test_code.py)
- [newcombotest.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/newcombotest.py)
- [ULN2803.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/ULN2803.py)
- [Toothpaste_squeezer.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Toothpaste_squeezer.py)

### I2C LCD Display and Library
We used the [LCD I2C display library](https://github.com/sterlingbeason/LCD-1602-I2C) and modified it to fit our project’s needs. See [LCD.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/LCD.py) and [lcd_test.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/lcd_test.py) for reference. The Inland I2C module (based on PCF 85174) works fine at 3.3V on the PocketBeagle, even though documentation states it needs 5V. The SCL and SDA lines are connected to I2C1 on the PocketBeagle, and the I2C address is `0x27`. If using a different I2C module, ensure that the address and connections are updated accordingly.

### Rotary Encoder
We utilize the PocketBeagle’s built-in eQEP functionality for the rotary encoder. The relevant file is provided in the PocketBeagle’s `/sensors/` directory and also included here as [rotaryEncoder.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/rotaryEncoder.py). The rotary encoder has 20 steps per cycle.

### Stepper Motor
We are using two stepper motors in total. It’s recommended to test one motor first before incorporating the second. The Inland stepper motor kit includes a drive board that can operate on a 3.3V supply. Ensure you create a proper power supply rail since multiple devices (LCD, two motors, rotary encoder) will be powered simultaneously. The original code provided by PocketBeagle is in `ULN2003.py` (renamed and modified here as [ULN2803.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/ULN2803.py)). Compare it to our test code, [motor_testcode.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/motor_testcode.py), where we define GPIO pins and establish that 512 steps equate to a 90° rotation. Note that documentation from MicroCenter is not accurate for step-to-degree conversions, so we determined this experimentally.

### Testing and Integration
After initializing all components (two stepper motors, one rotary encoder, and one LCD display), we performed several combo tests:

1. **[Rotaryencoder_lcd.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Rotaryencoder_lcd.py)**  
   Turning the rotary encoder updates the LCD with a calculated angle. This angle is only for demonstration and does not represent the physical angle of the encoder. The LCD updates only when the encoder’s value changes. Pressing the encoder’s button resets the displayed value to 0.

2. **[combo_test_code.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/combo_test_code.py)**  
   This code auto-refreshes the LCD and integrates the stepper motor. When the rotary encoder turns, the stepper motor rotates by a corresponding angle. Both direction and angle match the encoder’s movement. The button interrupt may not work perfectly, but you can stop the code from the Cloud9 IDE.

3. **[newcombotest.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/newcombotest.py)**  
   This test integrates two stepper motors. Each encoder step (4° per step on the LCD) corresponds to the motors, which have 512*4 steps per cycle. Approximately 4.5 encoder rotations correspond to a full motor rotation. Pressing the button resets the motors to their starting position. The LCD updates only when values change, and a `scale_factor` is introduced to account for speed differences. Two motors can move sequentially if defined separately; to move them simultaneously, define both controllers together. Note that reset may not work during motor movement—an issue explored later.

### Final Code: [Toothpaste_squeezer.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Toothpaste_squeezer.py)
The final code combines all features:

- Two stepper motors responding to the rotary encoder’s input.
- A `reset_motor_position()` function, though it’s not heavily used here.
- A `rotate_motors()` function with a loop checking for button presses.
- A `stop_motors()` function that displays "Stop!" when the button is pressed.
- Directional feedback: rotating the encoder clockwise displays "squeezing toothpaste!", and counterclockwise shows "releasing." Pressing the button stops the movement. Adjusting sleep times can improve responsiveness.

A basic mechanical prototype was modeled in Rhinoceros, and `.3dm` and `.stl` files are included in this repository. While not perfectly suited for real-world toothpaste squeezing, it demonstrates the concept and functionality.

---

*For an open-source project, consider adding contribution guidelines, licensing, and a code of conduct to foster a collaborative environment.*
