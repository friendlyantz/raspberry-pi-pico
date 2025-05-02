# for Python

on CircuitPython main script is called `code.py`, on MicroPython `main.py`

## PyCharm

### for CircuitPython

for finding usb device ` mpremote connect list` command from below can be useful
or just
```shell
ls /dev > temp.patch
diff <(ls /dev ) <(cat temp.patch ) | grep -E "^[<>]" | sed 's/[<>] //'
```

https://learn.adafruit.com/welcome-to-circuitpython/pycharm-and-circuitpython
https://www.youtube.com/watch?v=i7jEa2LyJtk

terminal IO for Mac/Pycharm `brew install tio`

```shell
circuitpython_setboard raspberry_pi_pico_w
```

## MicroPython Runner Installation
```sh
pip install mpremote
asdf reshim python # if you use `asdf` to install python for the binary to be in your path.
```

```sh
mpremote connect list
# /dev/cu.Bluetooth-Incoming-Port None 0000:0000 None None
# /dev/cu.usbmodem22201 e660583883807e27 2e8a:0005 MicroPython Board in FS mode
```
## REPL
```sh
mpremote connect port:/dev/cu.usbmodem22201
# Connected to MicroPython at /dev/cu.usbmodem22201
# Use Ctrl-] to exit this shell
>>>
```
https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf

- `CTRL-D` - to reboot
- `CTRL-]` - to exit

## Running commands
```
mpremote connect port:/dev/cu.usbmodem1301 run lib/hello_world.py
```

## Accessing files on Pico
__Run only REPL or RShell__
1. install `rshell` - Remote MictoPython shell is required # https://pypi.org/project/rshell/
  ```
pip install rshell
asdf reshim python # if using asdf

rshell -p <PATH_TO>
```
2. switch to `pyboard` storage
  ```
cd /pyboard
# cd /Users # to switch back
```

#### Syncing Files with Pico Internal storage

`rsync`
