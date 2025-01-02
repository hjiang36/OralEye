from gpiozero import Button, LED
import tkinter as tk
import socket
from PIL import Image, ImageTk
from picamera2 import Picamera2
import time

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

    def setup_gpio(self):
        """Setup GPIO using gpiozero."""
        # Buttons
        self.button_take_photo = Button(17)
        self.button_take_photo.when_pressed = self.capture_photo

        # LEDs
        self.led_red = LED(16)
        self.led_green = LED(20)
        self.led_blue = LED(21)

        # Buttons to control LEDs
        self.button_red_led = Button(22)
        self.button_green_led = Button(23)
        self.button_blue_led = Button(27)

        # Toggle LEDs on button press
        self.button_red_led.when_pressed = self.toggle_led(self.led_red)
        self.button_green_led.when_pressed = self.toggle_led(self.led_green)
        self.button_blue_led.when_pressed = self.toggle_led(self.led_blue)

    def toggle_led(self, led):
        """Returns a function that toggles the specified LED."""
        def _toggle():
            if led.is_lit:
                led.off()
            else:
                led.on()
        return _toggle

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

    def on_close(self):
        """Stops the camera and closes the application."""
        self.picam.stop()
        self.root.destroy()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()