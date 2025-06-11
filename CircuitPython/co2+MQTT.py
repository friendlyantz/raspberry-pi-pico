import time
import board
import busio
import adafruit_scd30
import adafruit_ssd1306
import microcontroller

import adafruit_minimqtt.adafruit_minimqtt as MQTT
import ssl

import json
import gc

# wifi
import os
import ipaddress
import wifi
import socketpool

# Import secrets
try:
    from secrets import WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD
except ImportError:
    print("WiFi and MQTT secrets are kept in secrets.py, please add them there!")
    raise

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
oled.text("booting...", 22,22, True)
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

scd.self_calibration_enabled = True
print("Self-calibration enabled:", scd.self_calibration_enabled)

# scd.ambient_pressure = 1100
print("Ambient Pressure:", scd.ambient_pressure)

# scd.altitude = 100
print("Altitude:", scd.altitude, "meters above sea level")

scd.forced_recalibration_reference = 409
print("Forced recalibration reference:", scd.forced_recalibration_reference)
print("")

oled.fill(0)
oled.text('connecting', 0, 20, True)
oled.show()

WIFI_TIMEOUT = 10
start_time = time.monotonic()
attempt_count = 0
MAX_ATTEMPTS = 5

try:
    while attempt_count < MAX_ATTEMPTS:
        attempt_count += 1
        try:
            oled.fill(0)
            oled.text(f'WiFi try {attempt_count}/{MAX_ATTEMPTS}', 0, 20, True)
            oled.show()
            wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
            break 
        except Exception as e:
            if time.monotonic() - start_time > WIFI_TIMEOUT or attempt_count >= MAX_ATTEMPTS:
                oled.fill(0)
                oled.text('WiFi failed', 0, 20, True)
                oled.text('Rebooting...', 0, 30, True)
                oled.show()
                time.sleep(3)
                import microcontroller
                microcontroller.reset()
          
            oled.fill(0)
            oled.text('WiFi retry', 0, 20, True)
            oled.text(f'Error: {str(e)[:16]}', 0, 30, True)
            oled.show()
            time.sleep(2)

    oled.fill(0)
    oled.text('WiFi Connected!', 0, 20, True)
    oled.text(f'{wifi.radio.ipv4_address}', 0, 30, True)
    oled.show()
    time.sleep(2)
except Exception as conn_error:
    oled.fill(0)
    oled.text('Fatal WiFi Error', 0, 20, True)
    oled.text('Rebooting...', 0, 30, True)
    oled.show()
    time.sleep(3)
    import microcontroller
    microcontroller.reset()




photocell_feed =  "CO2"


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    oled.fill(0)
    print("Disconnected from mqtt")
    oled.text('Disconnected from mqtt', 0, 30, True)
    oled.show()



def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    print(f"New message on topic {topic}: {message}")


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

mqtt_client = MQTT.MQTT(
    broker=MQTT_BROKER,
    port=MQTT_PORT,
    username=MQTT_USERNAME,
    password=MQTT_PASSWORD,
    socket_pool=pool,
    ssl_context=ssl_context,
)

mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

print("Connecting to mqtt")
mqtt_client.connect()
print(f"Connected to mqtt")
time.sleep(2)




while True:
    data = scd.data_available
    if data:
        oled.fill(0)
        print("Data Available!")
        mqtt_client.publish(photocell_feed, scd.CO2)
        print("CO2:", scd.CO2, "PPM")
        f_string = f"CO2: {scd.CO2:.2f}"
        oled.text(f_string, 0, 10, 1)
        
        print("Temperature:", scd.temperature, "degrees C")
        temperature_string = f"Temperature: {scd.temperature:.3f}"
        oled.text(temperature_string, 0, 20, True)
        
        print("Humidity::", scd.relative_humidity, "%%rH")
        rh_string = f"Humidity: {scd.relative_humidity:.2f}"
        oled.text(rh_string, 0, 30, True)

        measurement_int_string = f"interval: {scd.measurement_interval}"
        oled.text(measurement_int_string, 0, 50, True)
        oled.show()
        
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


        
        print("")
        print("Waiting for new data...")
        print("")

        

    time.sleep(2.5)

