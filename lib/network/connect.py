import network
import time
import rp2
import ubinascii
import urequests as requests

rp2.country('AU')

ssid = 'NETWROK'
password = 'password'

wlan = network.WLAN(network.STA_IF)
wlan.active(True) # non power-saving
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print(mac)
    print(f"Channel: {wlan.config('channel')}")
    print(wlan.config('essid'))
    print(wlan.config('txpower'))
          
    
#// Return value of cyw43_wifi_link_status
#define CYW43_LINK_DOWN (0)
#define CYW43_LINK_JOIN (1)
#define CYW43_LINK_NOIP (2)
#define CYW43_LINK_UP (3)
#define CYW43_LINK_FAIL (-1)
#define CYW43_LINK_NONET (-2)
#define CYW43_LINK_BADAUTH (-3)


# HTTP with sockets
import socket

ai = socket.getaddrinfo("google.com", 80)
addr = ai[0][-1]

# Create a socket and make a HTTP request
s = socket.socket()
s.connect(addr)
s.send(b"GET / HTTP/1.0\r\n\r\n")

# Print the response
print(s.recv(512))

# HTTP with urequests


r = requests.get("http://www.google.com")
print(r.content)
# r.json() # limited support. commented out since it wasn't working
r.close() # garbage-collection

r = requests.get("http://www.raspberrypi.com")
print(r.status_code)
r.close() # garbage-collection

while True:
    # Do things here, perhaps measure something using a sensor?

    # ...and then define the headers and payloads
    headers = 1
    payload = 2

    # Then send it in a try/except block
    try:
        print("sending...")
        response = requests.post("A REMOTE END POINT", headers=headers, data=payload)
        print("sent (" + str(response.status_code) + "), status = " + str(wlan.status()) )
        response.close()
    except:
        print("could not connect (status =" + str(wlan.status()) + ")")
        if wlan.status() < 0 or wlan.status() >= 3:
            print("trying to reconnect...")
            wlan.disconnect()
            wlan.connect(ssid, password)
            if wlan.status() == 3:
                print('connected')
            else:
                print('failed')
    time.sleep(5)
