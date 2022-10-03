from machine import Pin, Timer
import _thread
from time import sleep

led = Pin('LED', Pin.OUT)
baton = _thread.allocate_lock()
sleep_time = 0.5
tim = Timer()

def tick(timer):
    global led
    led.toggle()

song = ""

def verse(counter):
    if counter > 2:
        return """
{} bottles of beer on the wall, {} bottles of beer.
Take one down and pass it around, {} bottles of beer on the wall.
""".format(counter, counter, counter - 1)
    
    
def test_the_first_verse():
    expected = """
99 bottles of beer on the wall, 99 bottles of beer.
Take one down and pass it around, 98 bottles of beer on the wall.
"""
    spec_presenter(verse(99), expected)


def test_another_verse():
    'pending'

def spec_presenter(subject, expected):
    if subject == expected:
        print("SUCCESS!")
        print(expected)
        led.on()
    else:
        print('--------- FAIL. expected: --------')
        print(expected)
        print('VS')
        print(subject)
        tim.init(freq=10, mode=Timer.PERIODIC, callback=tick)

    
def run_all_specs():
    test_the_first_verse()
    led.on()
        
    
run_all_specs()