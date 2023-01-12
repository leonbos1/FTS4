from hcsr04 import HCSR04
from time import sleep
from machine import Pin, ADC
import urequests
import json

def main():	
    ENVIRONMENT = 'production'
    #ENVIRONMENT = 'development'
    #ENVIRONMENT = 'debug'
    if ENVIRONMENT != 'debug':
        do_connect(ENVIRONMENT=ENVIRONMENT)
    # ESP32
    sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)
    sound = ADC(Pin(34))
    sound.atten(ADC.ATTN_11DB)
    sound.width(ADC.WIDTH_12BIT)

    while True:
        try:
            distance = sensor.distance_cm()
            soundread = sound.read()

            object = {
                'sensor_id': 1,
                'distance': distance,
                'sound': soundread
            }

            if ENVIRONMENT != 'debug':
                post_data(object, ENVIRONMENT)

            else:
                print(object)
            sleep(1)

        except Exception as e:
            print(e)
            sleep(1)
    
def do_connect(ENVIRONMENT: str):
    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('connecting to network...')

        if ENVIRONMENT == 'production':
            wlan.connect('kaas', '12121212')
        elif ENVIRONMENT == 'development':
            wlan.connect('fam.bos', 'Stroopwafels1')

        while not wlan.isconnected():
            pass

    print('network config:', wlan.ifconfig())

def post_data(obj, ENVIRONMENT: str):
    if ENVIRONMENT == 'production':
        url = "http://ronleon.nl:2000/measurement"
    else:
        url = "http://127.0.0.1:2000/measurement"

    payload = json.dumps(obj)
    response = urequests.post(url,data=payload)
    print(response.status_code)
    
if __name__ == "__main__":
    main()
