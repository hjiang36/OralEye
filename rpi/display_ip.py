import tkinter as tk
import socket
from PIL import Image, ImageTk
from picamera2 import Picamera2

import RPi.GPIO as GPIO
import time
from threading import Thread

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address and Camera Preview")
        self.root.geometry("240x240")
        self.root.configure(bg="black")

        # Display IP Address
        ip_address = self.get_ip_address()
        self.label = tk.Label(root, text=f"IP: {ip_address}", fg="white", bg="black", font=("Arial", 10))
        self.label.pack(pady=10)

        # Create a canvas for the live camera feed
        self.canvas = tk.Canvas(root, width=240, height=160, bg="black")
        self.canvas.pack()

        # Initialize Picamera2
        self.picam = Picamera2()
        self.picam_config = self.picam.create_preview_configuration(main={"size": (640, 480)})
        self.picam.configure(self.picam_config)
        self.picam.start()

        # Setup GPIO
        self.setup_gpio()

        # Update camera preview
        self.update_camera()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start GPIO event listener in a separate thread
        self.gpio_thread = Thread(target=self.monitor_gpio, daemon=True)
        self.gpio_thread.start()

    def setup_gpio(self):
        """Setup GPIO pins for buttons and LEDs."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Button pins
        self.button_pin_take_photo = 17
        self.button_pin_led_red = 22
        self.button_pin_led_green = 23
        self.button_pin_led_blue = 27

        # LED pins
        self.led_red = 16
        self.led_green = 20
        self.led_blue = 21

        # Setup button pins as input with pull-up resistors
        GPIO.setup(self.button_pin_take_photo, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_pin_led_red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_pin_led_green, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_pin_led_blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup LED pins as output
        GPIO.setup(self.led_red, GPIO.OUT)
        GPIO.setup(self.led_green, GPIO.OUT)
        GPIO.setup(self.led_blue, GPIO.OUT)

        # Initialize LEDs to OFF
        GPIO.output(self.led_red, GPIO.LOW)
        GPIO.output(self.led_green, GPIO.LOW)
        GPIO.output(self.led_blue, GPIO.LOW)

    def get_ip_address(self):
        """Fetches the local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception:
            ip_address = "No network"
        return ip_address

    def update_camera(self):
        """Captures a frame from the camera and updates the tkinter canvas."""
        frame = self.picam.capture_array()
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

        # Schedule the next frame update
        self.root.after(10, self.update_camera)

    def capture_photo(self):
        """Captures a photo and saves it to disk."""
        filename = f"photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
        self.picam.capture_file(filename)
        print(f"Photo saved to {filename}")

    def toggle_led(self, led_pin):
        """Toggles the state of the specified LED."""
        current_state = GPIO.input(led_pin)
        GPIO.output(led_pin, not current_state)
        print(f"LED on pin {led_pin} is now {'ON' if not current_state else 'OFF'}")

    def monitor_gpio(self):
        """Monitors GPIO buttons for events."""
        while True:
            if GPIO.input(self.button_pin_take_photo) == GPIO.LOW:
                print("Take Photo button pressed")
                self.capture_photo()
                time.sleep(0.5)  # Debounce delay

            if GPIO.input(self.button_pin_led_red) == GPIO.LOW:
                print("Red LED button pressed")
                self.toggle_led(self.led_red)
                time.sleep(0.5)

            if GPIO.input(self.button_pin_led_green) == GPIO.LOW:
                print("Green LED button pressed")
                self.toggle_led(self.led_green)
                time.sleep(0.5)

            if GPIO.input(self.button_pin_led_blue) == GPIO.LOW:
                print("Blue LED button pressed")
                self.toggle_led(self.led_blue)
                time.sleep(0.5)

    def on_close(self):
        """Stops the camera, cleans up GPIO, and closes the application."""
        self.picam.stop()
        GPIO.cleanup()
        self.root.destroy()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()