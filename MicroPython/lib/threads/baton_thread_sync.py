from machine import Pin
import _thread
import utime

led = Pin('LED', Pin.OUT)

baton = _thread.allocate_lock()

def core1():
    delay = 1
    while True:
        print("------SECOND THREAD LOOP START-------")
        baton.acquire() # takeover from main THREAD
        
        print("BATON -> 2")
        utime.sleep(delay) # this doesn't sleep inline
        
        print('SECOND THREAD slept a bit.')
        utime.sleep(delay) # this doesn't sleep inline
        
        print('SECOND THREAD slept a bit again...')
        utime.sleep(delay) # this doesn't sleep inline

        print("2 -> BATON")
        utime.sleep(delay)
        
        baton.release() # giveaway lock
    
second_thread = _thread.start_new_thread(core1, ()) # SECOND thread  
while True: # MAIN THREAD that CAN hold baton to SECOND THREAD
    print('================MAIN LOOP START===============')
    baton.acquire()  # hold SECOND exec
    print("BATON -> M")
    for x in range(1, 50, 5):
        led.on()
        print('fixin...')
        utime.sleep(0.01)

        led.off()
        utime.sleep(0.2)
    print("M -> BATON")
    baton.release() # return to MAIN THREAD
    
    utime.sleep(1) # gixing time for other thread to print MSG, otherwise below MSG will be concatinated
    for x in range(1, 20):
        print('--z-z-z-z-z-z--z-z-z-------------MAIN SLEEPs---no baton--')
        utime.sleep(1)
    print('--MAIN WAKES---------------------still no baton, will takeover in 2--')
    utime.sleep(2)
 