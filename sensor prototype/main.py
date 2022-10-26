from hcsr04 import HCSR04
from time import sleep
import urequests
import json

def main():	
    do_connect()
    # ESP32
    sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

    # ESP8266
    #sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)

    while True:
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
        post_data(distance)
        sleep(1)
    
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('kaas', '12121212')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def post_data(distance):
    url = "http://ronleon.nl:2000/distance"
    payload = {
        'distance':distance
        }
    payload = json.dumps(payload)
    
    response = urequests.post(url,data=payload)

    print(response.text)

    
if __name__ == "__main__":
    main()

    




