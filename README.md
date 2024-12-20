# ENGI301
Repository for ENGI301 course work

## Project-1
The project is all about building a toothpaste squeezer based on the **PocketBeagle**. The **Cloud9 IDE** is where we write code and test everything.

### Hardware Components
Most parts are ordered from **Inland at MicroCenter**. We used:  
- **Rotary Encoder**: [Module Link](https://community.microcenter.com/kb/articles/640-inland-rotary-encoder-module), [Shop Link](https://www.microcenter.com/product/618904/inland-ks0013-keystudio-rotary-encoder-module)  
- **Step Motor (28BYJ-48) with ULN 2003a Drive Board**: [Module Link](https://community.microcenter.com/kb/articles/675-inland-stepper-motor-drive-board-5v-stepper-motor-3pcs), [Shop Link](https://www.microcenter.com/product/639726/inland-ks0327-keyestudio-stepper-motor-drive-board-5v-stepper-motor-kit-(3pcs))  
- **1602 I2C Display Module**: [Module Link](https://community.microcenter.com/kb/articles/649-inland-1602-i2c-module), [Shop Link](https://www.microcenter.com/product/632704/inland-1602-i2c-lcd-display-module)

### LCD I2C Display
The LCD I2C display library was taken from [here](https://github.com/sterlingbeason/LCD-1602-I2C), and I made some changes to fit our project.  
Please find [LCD.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/LCD.py) and [lcd_test.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/lcd_test.py) in the repository.

The I2C module we have is designed by Inland based on **PCF 85174**. Although the PocketBeagle only has 3.3V Vcc and Inland says it needs 5V, it works fine with 3.3V. **SCL** and **SDA** are connected to I2C1 on the PocketBeagle, and the address is **0x27**. If you use a different I2C module, please ensure the address and connections are updated correctly.

**Remember**: When you later run test code or final code, keep all files in the same folder so you can import them easily.

### Rotary Encoder
For the rotary encoder, we use the **eQEP** function provided by the PocketBeagle. The file is provided by PocketBeagle and is in our Cloud9 IDE under `/sensors/`. We will also provide it in our repository as [rotaryEncoder.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/rotaryEncoder.py).

### Step Motor
For the step motor, the project involves using two motors.  
I recommend testing one motor first to ensure it works properly before adding the second. The **Inland 3-piece step motor kit** comes with a drive board that automatically adjusts the voltage to what the motor needs from the 3.3V we provide.

**Note**: The Vcc and GND pins on the PocketBeagle might not be enough since we have four devices. Please create a proper power supply rail.

The original code is provided by PocketBeagle as `ULN2003.py` (we provide a similar file [ULN2803.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/ULN2803.py) for reference), but it won’t work properly without modifications. I made some changes to the original file, and it’s now named [motor_testcode.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/motor_testcode.py).

In this code, you will find where I attached the motor controller pins: `["47", "64", "46", "44"]` (GPIO numbers). The step motor will turn **90 degrees with 512 steps**. The info provided by the MicroCenter community webpage was not accurate about degrees per step, so we determined it experimentally.

### Combo Tests
After initializing all three main components (actually four devices, since we have two motors), we will perform some combo tests to ensure that communication between each device works well and to lay some groundwork for our final project.

1. **[Rotaryencoder_lcd.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Rotaryencoder_lcd.py)**:  
   This program shows how rotating the rotary encoder updates the I2C LCD display with a calculated angle based on how many steps the encoder has moved.  
   - The displayed angle does not correspond to the actual physical angle of the encoder; it’s just a test value.  
   - The rotary encoder has **20 steps per cycle**.  
   - The LCD updates only after turning the rotary encoder. If it’s not turned, the LCD does not refresh.  
   - Pressing the rotary encoder button clears and resets the displayed value to 0.

2. **[combo_test_code.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/combo_test_code.py)**:  
   This code keeps the auto-refresh display function from `Rotaryencoder_lcd.py` but does not utilize the encoder’s push button. In a future test code (#3), we will introduce the button reset function.  
   - Here, the step motor will turn by the angle displayed on the LCD once the rotary encoder is turned.  
   - The motor and encoder should rotate in the same direction.  
   - The `KeyBoarInterrupt` function may not work perfectly, but it doesn’t affect much. You can press the stop button at any time in the Cloud9 IDE.

3. **[newcombotest.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/newcombotest.py)**:  
   This test includes **2 step motors**.  
   - The rotary encoder has 20 steps per cycle, and each step represents **4 degrees on the LCD display**.  
   - The step motor has **512*4 steps per cycle**.  
   - When the rotary encoder moves one step, the motor moves 4 degrees in the same direction. Thus, **4.5 cycles of the rotary encoder = one full revolution of the motor**.  
   - Pressing the rotary encoder’s button moves the step motor back to its original position.  
   - The LCD display now auto-refreshes only when values change.  
   - We introduce a `scale_factor` because the step motor moves slower than the encoder rotation.  
   - If you write the code yourself, pay attention to how you define controller functions for two motors. Defining them in sequence causes sequential movement, while defining them together allows simultaneous movement.  
   - `reset_motor_position` returns both motors to their original positions when you press the rotary encoder’s button, but it won’t work while the motors are moving. We’ll handle this issue in the final code.  
   - Both motors move in different directions here, and the LCD shows values that don’t necessarily have real meaning—they just scale proportionally with steps. You can modify `scale_factor` and displayed values to make them align better if needed.

### Final Code
**[Toothpaste_squeezer.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Toothpaste_squeezer.py)**:  
This final code uses the two-step motor functions from test code #3.  
- We still have `reset_motor_position()` here, but we won’t use it.  
- The main difference is in the `rotate_motors` definition, where we now have a loop checking if the button is pressed.  
- We must include this check within the `rotate_motors` loop; otherwise, the motor will just stop after completing its motion.  
- We also have `stop_motors()` to display "Stop!" on the LCD when the button is pressed.  
- The first step motor is on the left, the second on the right. Turning the rotary encoder clockwise displays "squeezing toothpaste!", and turning it the other way shows "releasing". Pressing the button stops the motion immediately.  
- If the button is pressed extremely fast, it may not stop instantly, but normally it’s fine. Adjusting the sleep time or timing between functions can improve accuracy.  
- A basic model was designed in **Rhinoceros** so you can assemble all the devices.  
  - **Note**: It’s just a prototype for testing functions and presenting the basic idea, not a fully functional toothpaste squeezer.  
  - `.3dm` and `.stl` files are included in the repository for reference.

