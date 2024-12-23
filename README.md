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
For the step motor, the project involves using two motors. I recommend testing one motor first to ensure it works properly before adding the second. The Inland 3-piece step motor kit comes with a drive board that automatically adjusts the supply to what the motor needs from the 3.3V we provide. Remember that the Vcc and GND pins on the PocketBeagle might not be enough since we have four devices. Please create a proper power supply rail. The original code is provided by PocketBeagle as ULN2003.py (we provide a similar file [ULN2803.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/ULN2803.py) for reference), but it won’t work properly without modifications. I made some changes to the original file, it's named as [motor_testcode.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/motor_testcode.py). In this code, you will find where I attached the motor controller pins = ["47", "64", "46", "44"] (GPIO numbers). The step motor will turn 90 degrees with 512 steps. The info provided by the MicroCenter community webpage was not accurate about degrees per step, so we determined it experimentally.

### Combo Tests
After initializing all three main components (actually four devices since we have two motors), we will perform some combo tests to ensure that communication between each device works well and to lay some groundwork for our final project.

1. **[Rotaryencoder_lcd.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Rotaryencoder_lcd.py)**: 
 This program shows how rotating the rotary encoder updates the I2C LCD display with a calculated angle based on how many steps the encoder has moved. Note that the displayed angle does not correspond to the actual physical angle of the encoder; it’s just a test value. The rotary encoder has 20 steps per cycle. In the main loop, the LCD updates only after turning the rotary encoder. If it’s not turned, the LCD does not refresh, which I found more comfortable to read. If your project needs continuous updates, refer to this code. Pressing the rotary encoder button clears and resets the displayed value to 0.

2. **[combo_test_code.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/combo_test_code.py)**:  
Next, this code keeps the auto-refresh display function from Rotaryencoder_lcd.py but does not utilize the encoder’s push button. In test code #3, we will introduce the button reset function. In combo_test_code.py, the step motor will turn by the angle displayed on the LCD once the rotary encoder is turned. The motor and the encoder should rotate in the same direction. The KeyBoarInterrupt function may not work perfectly, but it won’t affect much. You can press the stop button at any time in the Cloud9 IDE.

3. **[newcombotest.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/newcombotest.py)**:  
For test code #3, we include **2 step motors**. Recall that the rotary encoder has 20 steps per cycle, and each step represents 4 degrees on the LCD display. The step motor has 512*4 steps per cycle. I made it so that when the rotary encoder moves one step (clockwise or counterclockwise), the motor moves 4 degrees in the same direction. Thus, 4.5 cycles of the rotary encoder will make the motor turn one full revolution. Pressing the rotary encoder’s button moves the step motor back to the original position. The LCD display also has an auto-refresh function that only updates when values change. This time we introduce a scale_factor because the step motor moves much slower compared to the encoder’s rotation. We are now better prepared for our final code since we don’t want the toothpaste squeezer to require many encoder turns. If you write the code yourself, note how to define controller functions when using two motors. You can define each controller and use them in sequence, causing sequential motor movement, or define both controllers together for simultaneous movement. Here we also have reset_motor_position—both motors return to their original positions when you press the rotary encoder’s button. However, it won’t work while the motors are moving. A similar problem will appear in the final code, and we’ll see how to address it. Also, in this test, the two motors move in different directions. The LCD still shows some values, but they don’t mean much; the angles just increase proportionally with the step motor and rotary encoder movements. We want to ensure the LCD I2C display works with newly programmed functions. You can modify scale_factor and the displayed values to make them align better—it’s an easy step.

### Final Code
**[Toothpaste_squeezer.py](https://github.com/BornForVR/ENGI-301---Project-1/blob/main/Toothpaste_squeezer.py)**:  
In this final code we use the two step motor functions from test code #3. We still have reset_motor_position() here, but we won’t use it. The main difference is under the rotate_motors definition. We now have a simple loop checking whether the button is pressed. We must include it inside the rotate_motors function’s loop; otherwise, the motor will stop after completing its motion without any change. We also have stop_motors() to show a "Stop!" message on the display when the button is pressed. I put the first step motor on the left and the second on the right so that when we turn the rotary encoder clockwise, it displays "squeezing toothpaste!", and when we turn it the other way, it displays "releasing". Pressing the button stops it immediately. It may not stop if you press the button extremely fast, but normally it’s fine. To improve accuracy, you can adjust the button’s sleep time and the timing between functions. I designed a basic model in Rhinoceros so you can assemble all the devices. Don’t expect it to work perfectly with actual toothpaste, as it’s just a prototype to test functions and present the basic idea. I’ve included the .3dm and .stl files in the repository. You can check them out.

## Acknowledgments
We extend our deepest gratitude to Professor Erik Welsh, our esteemed instructor for ENGI 301, whose guidance and expertise were invaluable throughout the course of this project.
