import time
import board
import busio
import adafruit_scd30
import adafruit_ssd1306

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
# NOTE: CircuitPython and MicroPython pinout if different.
# CircuitPython:
# SCL = GP5
# SDA = GP4
i2c = busio.I2C(board.GP5, board.GP4, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)
time.sleep(0.5) # Wait a bit for the sensor to boot up
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("lalal", 22,22, True)
oled.show()

import digitalio
BEEPER_PIN = digitalio.DigitalInOut(board.GP22)
BEEPER_PIN .direction = digitalio.Direction.OUTPUT


LED_1 = digitalio.DigitalInOut(board.GP18)
LED_1 .direction = digitalio.Direction.OUTPUT
LED_2 = digitalio.DigitalInOut(board.GP19)
LED_2 .direction = digitalio.Direction.OUTPUT
LED_3 = digitalio.DigitalInOut(board.GP20)
LED_3 .direction = digitalio.Direction.OUTPUT
LED_4 = digitalio.DigitalInOut(board.GP21)
LED_4 .direction = digitalio.Direction.OUTPUT

# scd.temperature_offset = 10
print("Temperature offset:", scd.temperature_offset)

# scd.measurement_interval = 4
print("Measurement interval:", scd.measurement_interval)

# scd.self_calibration_enabled = True
print("Self-calibration enabled:", scd.self_calibration_enabled)

# scd.ambient_pressure = 1100
print("Ambient Pressure:", scd.ambient_pressure)

# scd.altitude = 100
print("Altitude:", scd.altitude, "meters above sea level")

# scd.forced_recalibration_reference = 409
print("Forced recalibration reference:", scd.forced_recalibration_reference)
print("")

while True:
    data = scd.data_available
    if data:
        oled.fill(0)
        print("Data Available!")
        print("CO2:", scd.CO2, "PPM")
        f_string = f"CO2: {scd.CO2:.2f}"
        oled.text(f_string, 0, 10, 1)
        if scd.CO2 > 1000.0:
            BEEPER_PIN.value = 1
            time.sleep(0.2)
            BEEPER_PIN.value = 0
            time.sleep(0.2)
            BEEPER_PIN.value = 1
            time.sleep(0.2)
            BEEPER_PIN.value = 0
            time.sleep(0.2)
            BEEPER_PIN.value = 1
            time.sleep(0.1)
            BEEPER_PIN.value = 0
            LED_1.value = 1
            LED_2.value = 1
            LED_3.value = 1
            LED_4.value = 1
        elif scd.CO2 > 900.0:
            BEEPER_PIN.value = 1
            time.sleep(0.1)
            BEEPER_PIN.value = 0
            time.sleep(0.1)
            BEEPER_PIN.value = 1
            time.sleep(0.1)
            BEEPER_PIN.value = 0
            LED_1.value = 1
            LED_2.value = 1
            LED_3.value = 1
            LED_4.value = 0
        elif scd.CO2 > 800.0:
            BEEPER_PIN.value = 1
            time.sleep(0.1)
            BEEPER_PIN.value = 0
            LED_1.value = 1
            LED_2.value = 1
            LED_3.value = 0
            LED_4.value = 0
        elif scd.CO2 > 700.0:
            LED_1.value = 1
            LED_2.value = 0
            LED_3.value = 0
            LED_4.value = 0
        else:
            LED_1.value = 0
            LED_2.value = 0
            LED_3.value = 0
            LED_4.value = 0



        print("Temperature:", scd.temperature, "degrees C")
        temperature_string = f"Temperature: {scd.temperature:.3f}"
        oled.text(temperature_string, 0, 20, True)
        print("Humidity::", scd.relative_humidity, "%%rH")
        rh_string = f"Humidity: {scd.relative_humidity:.2f}"
        oled.text(rh_string, 0, 30, True)
        print("")
        print("Waiting for new data...")
        print("")
        measurement_int_string = f"interval: {scd.measurement_interval}"
        oled.text(measurement_int_string, 0, 50, True)
        oled.show()

    time.sleep(2.5)