from hcsr04 import HCSR04
from time import sleep
from machine import Pin, ADC
import urequests
import json

def main():	
    do_connect()
    # ESP32
    sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
    sound = ADC(Pin(34))
    sound.atten(ADC.ATTN_11DB)
    sound.width(ADC.WIDTH_12BIT)

    while True:
        distance = sensor.distance_cm()
        print('Distance:', distance, 'cm')
        soundread = sound.read()
        print('Sound:', soundread)

        object = {
            'distance': distance,
            'sound': soundread
        }
        post_data(object)
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

def post_data(obj):
    url = "http://ronleon:2000/distance"

    payload = json.dumps(obj)
    
    response = urequests.post(url,data=payload)

    print(response.text)

    
if __name__ == "__main__":
    main()

    






