import time
import board
import busio
import adafruit_scd30

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
# NOTE: CircuitPython and MicroPython pinout if different.
# CircuitPython:
# SCL = GP5
# SDA = GP4
i2c = busio.I2C(board.GP5, board.GP4, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)