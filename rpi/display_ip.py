from gpiozero import Button, LED
import tkinter as tk
import socket
from PIL import Image, ImageTk, ImageOps, ImageDraw
from picamera2 import Picamera2
import time
import threading

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address and Camera Preview")
        self.root.overrideredirect(True)
        self.root.geometry("240x320+0+0")
        self.root.configure(bg="black")

        # Add an Exit button
        self.exit_button = tk.Button(
            root,
            text="X",
            command=self.on_close,  # Call on_close to clean up and exit
            font=("Arial", 10),
            bg="black",
            fg="white"
        )
        self.exit_button.place(x=200, y=10, width=40, height=24)

        # Display IP Address
        ip_address = self.get_ip_address()
        self.label = tk.Label(root, text=f"IP: {ip_address}", fg="white", bg="black", font=("Arial", 10))
        self.label.place(x=0, y=10, width=200, height=24)

        # Create a canvas for the live camera feed
        self.canvas_width, self.canvas_height = 420, 300
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.place(x=0, y=30)

        # Initialize Picamera2
        self.picam = Picamera2()
        self.camera_id = 0
        self.camera_lock = threading.Lock()
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
        self.led_laser = LED(16)
        self.led_white = LED(20)
        self.led_blue = LED(21)

        # Buttons to control LEDs
        self.button_laser_led = Button(22)
        self.button_white_led = Button(23)
        self.button_camera_swtich = Button(27)

        # Toggle LEDs on button press
        self.button_laser_led.when_pressed = self.toggle_led(self.led_laser)
        self.button_white_led.when_pressed = self.toggle_led(self.led_white)
        self.button_camera_swtich.when_pressed = self.switch_camera

    def toggle_led(self, led):
        """Returns a function that toggles the specified LED."""
        def _toggle():
            if led.is_lit:
                led.off()
            else:
                led.on()
        return _toggle
    
    def configure_camera(self, camera_id):
        """Configure the camera to use the specified camera_id"""
        if camera_id == self.camera_id:
            return  # No need to reconfigure if the camera is already selected
        camera_name = Picamera2.global_camera_info()[camera_id]["CameraName"]
        self.picam = Picamera2(camera_name)  # Reinitialize Picamera2 with selected camera
        self.picam.configure(self.picam.create_preview_configuration())
        self.picam.start()

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
    
    def switch_camera(self):
        """Switch between camera 0 and 1"""
        self.camera_id = 1 - self.camera_id  # Toggle between 0 and 1
        print(f"Switched to Camera {self.camera_id}")
        self.configure_camera(self.camera_id)

    def update_camera(self):
        """Captures a frame from the camera and updates the tkinter canvas."""
        with self.camera_lock:
            frame = self.picam.capture_array()
            image = Image.fromarray(frame)

        # Rotate the image 90 degrees
        image = image.rotate(-90, expand=True)

        # Resize the image to fit the canvas while maintaining aspect ratio
        image = ImageOps.contain(
            image, (self.canvas_width, self.canvas_height))

        # Draw a red crosshair in the center
        draw = ImageDraw.Draw(image)
        center_x, center_y = image.width // 2, image.height // 2
        crosshair_length = min(image.width, image.height) // 10
        line_width = 3

        # Draw horizontal and vertical lines
        draw.line((center_x - crosshair_length, center_y, center_x + crosshair_length, center_y), fill="red", width=line_width)
        draw.line((center_x, center_y - crosshair_length, center_x, center_y + crosshair_length), fill="red", width=line_width)


        # Convert the resized image to a format tkinter can display
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

        # Schedule the next frame update
        self.root.after(33, self.update_camera)

    def capture_photo(self):
        """Captures a photo and saves it to disk."""
        # Toggle the white LED on for a brief moment
        self.led_white.on()
        filename = f"photo_{time.strftime('%Y%m%d_%H%M')}_white.jpg"
        self.picam.capture_file(filename)
        self.led_white.off()

        # Toggle the blue LED on for a brief moment
        self.led_blue.on()
        filename = f"photo_{time.strftime('%Y%m%d_%H%M')}_blue.jpg"
        self.picam.capture_file(filename)
        self.led_blue.off()

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