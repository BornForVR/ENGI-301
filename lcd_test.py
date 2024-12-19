import time
from LCD import LCD

lcd = LCD(1, 0x27, True) # params available for I2C bus, I2C Address, and backlight on/off
            # lcd = LCD(2, 0x3F, True)

lcd.message("Hello World!", 1) # display 'Hello World!' on line 1 of LCD

time.sleep(5) # wait 5 seconds

lcd.clear() # clear LCD display