from machine import Pin
import _thread
from time import sleep
led = Pin('LED', Pin.OUT)
run_core1 = False    

def core0():
    global run_core1
    counter = 0
    msg = 'core0 count: '
    while True:
        for loop in range(5):
            print(f'{msg}{counter}')
            counter += 1
            sleep(1)
        
        run_core1 = True

        while run_core1:
            pass
    
def core1():
    global run_core1
    counter = 0
    msg = 'core1 count --->'
    while True:
        while not run_core1:
            pass
    
        print(f'{msg}{counter}')
        counter += 1
        sleep(1)
        
        run_core1 = False



second_thread = _thread.start_new_thread(core1, ())
core0()


