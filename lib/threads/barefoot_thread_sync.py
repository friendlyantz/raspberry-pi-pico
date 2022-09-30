from machine import Pin
import _thread
import utime

led = Pin('LED', Pin.OUT)
led.on()

build_is_broken = False # savage / 'barefoot' sync method to sync cores. this method might cause havoc in other languages and you can shoot yourself in the foot
    
def break_build():
    counter = 0
    while True:
        global build_is_broken
        counter += 1
        msg1 = "build is broken"
        msg2 = "build is FIXED"
        
        build_is_broken = True
        print(f'{msg1}{counter}{build_is_broken}')
        
        utime.sleep(2)
        
        build_is_broken = False
        print(f'{msg2}{counter}{build_is_broken}')
        utime.sleep(2)

def alarm_blinker():
    while True:
        while build_is_broken == True:
            led.on()
            utime.sleep(0.1)

            led.off()
            utime.sleep(0.1)


_thread.start_new_thread(break_build, ())
alarm_blinker()
