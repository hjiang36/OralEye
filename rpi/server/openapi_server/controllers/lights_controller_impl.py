# rpi/server/openapi_server/controllers/gpio_controller.py

import time
import RPi.GPIO as GPIO

# Globle config on MOCK mode
# In mock mode, we skip actual light control and return off always.
MOCK_MODE = True

# GPIO pin setup
RED_LASER_PIN = 18
BLUE_LED_PIN = 16
WHITE_LED_PIN = 20

# Disable GPIO in-use warnings
if not MOCK_MODE:
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_LASER_PIN, GPIO.OUT)
    GPIO.setup(WHITE_LED_PIN, GPIO.OUT)
    GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

    # Initial states (modify as needed)
    GPIO.output(RED_LASER_PIN, GPIO.LOW)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)
    GPIO.output(WHITE_LED_PIN, GPIO.LOW)

def set_light_status(white_led=None, blue_led=None, red_laser=None):
    if MOCK_MODE:
        return
    if white_led is not None:
        GPIO.output(WHITE_LED_PIN, GPIO.HIGH if white_led == 'on' else GPIO.LOW)
    if blue_led is not None:
        GPIO.output(BLUE_LED_PIN, GPIO.HIGH if blue_led == 'on' else GPIO.LOW)
    if red_laser is not None:
        GPIO.output(RED_LASER_PIN, GPIO.HIGH if red_laser == 'on' else GPIO.LOW)

def get_light_status():
    if MOCK_MODE:
        return {
            "white_led": "off",
            "blue_led": "off",
            "red_laser": "off"
        }
    return {
        "white_led": "on" if GPIO.input(WHITE_LED_PIN) else "off",
        "blue_led": "on" if GPIO.input(BLUE_LED_PIN) else "off",
        "red_laser": "on" if GPIO.input(RED_LASER_PIN) else "off"
    }

# Add a main function to test the GPIO controller
if __name__ == '__main__':
    print(get_light_status())
    
    # Turn on the white LED
    set_light_status(white_led='on', blue_led='off', red_laser='off')
    print(get_light_status())
    time.sleep(1)

    set_light_status(white_led='off', blue_led='on', red_laser='off')
    print(get_light_status())
    time.sleep(1)

    set_light_status(white_led='off', blue_led='off', red_laser='on')
    print(get_light_status())
    time.sleep(1)

    set_light_status(white_led='off', blue_led='off', red_laser='off')
    print(get_light_status())
