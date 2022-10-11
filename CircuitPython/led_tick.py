import board
import digitalio
from time import sleep

onboard_led = digitalio.DigitalInOut(board.LED)
onboard_led.direction = digitalio.Direction.OUTPUT

onboard_led.value = 0

# object <DigitalInOut> is of type DigitalInOut
#   deinit -- <function>
#   __enter__ -- <function>
#   __exit__ -- <function>
#   switch_to_output -- <function>
#   switch_to_input -- <function>
#   direction -- <property>
#   value -- <property>
#   drive_mode -- <property>
#   pull -- <property>


while True:
    sleep(1)
    print('tick')
    onboard_led.value = 1
    sleep(1)
    onboard_led.value = 0

