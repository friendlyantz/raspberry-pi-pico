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
    verse_template = """
{i} bottle{s} of beer on the wall, {i} bottle{s} of beer.
Take one down and pass it around, {left} bottle{last_s} of beer on the wall.
"""
    if counter > 2:
        return verse_template.format(i = counter, left = counter - 1, s = 's', last_s = 's')
    elif counter == 2:
        return verse_template.format(i = counter, left = counter - 1, s = 's', last_s = '')
    elif counter == 1:    
        return """
1 bottle of beer on the wall, 1 bottle of beer.
Take it down and pass it around, no more bottles of beer on the wall.
"""
    elif counter == 0:
        return """
No more bottles of beer on the wall, no more bottles of beer.
Go to the store and buy some more, 99 bottles of beer on the wall.
"""

def verses(start, finish):
    result = ""
    for i in range(start, finish -1, -1):
        result += verse(i)
    return result

def test_99_bottles_verse():
    expected = """
99 bottles of beer on the wall, 99 bottles of beer.
Take one down and pass it around, 98 bottles of beer on the wall.
"""
    spec_presenter(verse(99), expected)

def test_75_bottles_verse():
    expected = """
75 bottles of beer on the wall, 75 bottles of beer.
Take one down and pass it around, 74 bottles of beer on the wall.
"""
    spec_presenter(verse(75), expected)

def test_2_bottles_verse():
    expected = """
2 bottles of beer on the wall, 2 bottles of beer.
Take one down and pass it around, 1 bottle of beer on the wall.
"""
    spec_presenter(verse(2), expected)

def test_1_bottle_verse():
    expected = """
1 bottle of beer on the wall, 1 bottle of beer.
Take it down and pass it around, no more bottles of beer on the wall.
"""
    spec_presenter(verse(1), expected)

def test_no_bottles_verse():
    expected = """
No more bottles of beer on the wall, no more bottles of beer.
Go to the store and buy some more, 99 bottles of beer on the wall.
"""
    spec_presenter(verse(0), expected)

def test_couple_of_verses():
    expected = """
55 bottles of beer on the wall, 55 bottles of beer.
Take one down and pass it around, 54 bottles of beer on the wall.

54 bottles of beer on the wall, 54 bottles of beer.
Take one down and pass it around, 53 bottles of beer on the wall.
"""
    spec_presenter(verses(55,54), expected)

def test_last_three_verses():
    expected = """
2 bottles of beer on the wall, 2 bottles of beer.
Take one down and pass it around, 1 bottle of beer on the wall.

1 bottle of beer on the wall, 1 bottle of beer.
Take it down and pass it around, no more bottles of beer on the wall.

No more bottles of beer on the wall, no more bottles of beer.
Go to the store and buy some more, 99 bottles of beer on the wall.
"""
    spec_presenter(verses(2,0), expected)


def spec_presenter(subject, expected):
    if subject == expected:
        print("SUCCESS!")
        print(expected)
        led.on()
    else:
        tim.init(freq=10, mode=Timer.PERIODIC, callback=tick)
        raise Exception("""
EXPECETD:
{}
VS subject:
{}
""".format(expected, subject)
            )

def run_all_specs():
    test_99_bottles_verse()
    test_75_bottles_verse()
    test_2_bottles_verse()
    test_1_bottle_verse()
    test_no_bottles_verse()
    test_couple_of_verses()
    test_last_three_verses()
    tim.init(freq=0.5, mode=Timer.PERIODIC, callback=tick)
    
run_all_specs()