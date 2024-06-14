import RPi.GPIO as GPIO
import requests
import time

# Define GPIO pins for the buttons and the lights
BUTTON_WHITE_BLUE_PIN = 24
BUTTON_RED_LASER_PIN = 25

LIGHT_CONTROL_URL = "http://localhost:5000/api/lights"

# State variables for lights
white_blue_state = 0  # 0: off, 1: white, 2: blue
red_laser_state = False  # False: off, True: on

def rotate_white_blue():
    global white_blue_state
    white_blue_state = (white_blue_state + 1) % 3
    if white_blue_state == 0:
        action = {"light": "white_blue", "state": "off"}
    elif white_blue_state == 1:
        action = {"light": "white", "state": "on"}
    elif white_blue_state == 2:
        action = {"light": "blue", "state": "on"}
    return action

def toggle_red_laser():
    global red_laser_state
    red_laser_state = not red_laser_state
    action = {"light": "red_laser", "state": "on" if red_laser_state else "off"}
    return action

def button_callback(channel):
    if channel == BUTTON_WHITE_BLUE_PIN:
        action = rotate_white_blue()
    elif channel == BUTTON_RED_LASER_PIN:
        action = toggle_red_laser()
    response = requests.post(LIGHT_CONTROL_URL, json=action)
    if response.status_code == 200:
        print(f"Action {action} executed successfully")
    else:
        print(f"Failed to execute action {action}")

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_WHITE_BLUE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_RED_LASER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_WHITE_BLUE_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)
    GPIO.add_event_detect(BUTTON_RED_LASER_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

if __name__ == "__main__":
    try:
        setup()
        while True:
            time.sleep(1) # Keep the script running
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Button listener stopped")