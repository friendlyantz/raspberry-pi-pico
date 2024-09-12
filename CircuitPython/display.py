import board
import busio
import adafruit_ssd1306


SCL = board.GP5
SDA = board.GP4
i2c = busio.I2C(SCL, SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
# you need  font to be in root
# wget -O font5x8.bin https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/main/examples/font5x8.bin\?raw\=true
oled.text("lala", 33,33, 1)

oled.show()