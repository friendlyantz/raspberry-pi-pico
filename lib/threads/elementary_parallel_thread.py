from machine import Pin
import _thread
import utime

led = Pin('LED', Pin.OUT)
    
def core0():
    global run_core1
    counter = 0
    msg = 'core0 count: '
    while True:
        print(f'{msg}{counter}')
        counter += 1
        utime.sleep(3)
    
def core1():
    counter = 0
    msg = 'core1 count --->'
    while True:
        print(f'{msg}{counter}')
        counter += 1
        utime.sleep(1)

_thread.start_new_thread(core1, ())
core0()

