from machine import Pin, Timer
import _thread

led = Pin('LED', Pin.OUT)


def print_hello(timer):
    print('hello')


def tick(timer):
    global led
    led.toggle()


def regular_ticking():
    tim1 = Timer()
    tim1.init(freq=10, mode=Timer.PERIODIC, callback=tick)


def regular_greeting():
    tim2 = Timer()
    tim2.init(freq=0.5, mode=Timer.PERIODIC, callback=print_hello)


regular_greeting()
# regular_ticking()


