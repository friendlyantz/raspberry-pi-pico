from machine import Pin
import _thread
from time import sleep

led = Pin('LED', Pin.OUT)
baton = _thread.allocate_lock()
sleep_time = 0.5

def event_bus(baton_owner):
    msg = 'pooled message from: '
    print(f'{msg}{baton_owner}')
        
def core0():
    wait_counter = 0
    msg = 'core0 count: '
    while True:
        #print('BATON -> M')
        wait_counter = 0

        while not baton.acquire(0,1): # (waitflag = 1, timeout = 1)
            wait_counter += 1
            
        print("...CORE0 waited" + str(wait_counter))

        for c in 'CORE0':
            print("-" + str(c))
            sleep(sleep_time)
        baton.release()
def core1():
    msg = 'core1 count --->'
    while True:    
        baton.acquire()
        
        for c in 'core1':
            print(c)
            sleep(sleep_time*2)
        baton.release()

second_thread = _thread.start_new_thread(core1, ())
core0()
