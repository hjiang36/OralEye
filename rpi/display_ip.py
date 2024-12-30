import tkinter as tk
import socket
from PIL import Image, ImageTk
from picamera2 import Picamera2

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
        self.canvas = tk.Canvas(root, width=640, height=480, bg="black")
        self.canvas.pack()

        # Initialize Picamera2
        self.picam = Picamera2()
        self.picam_config = self.picam.create_preview_configuration(main={"size": (640, 480)})
        self.picam.configure(self.picam_config)
        self.picam.start()

        # Add Capture Button
        self.capture_button = tk.Button(
            root, text="Capture Photo", command=self.capture_photo, font=("Arial", 8), bg="green", fg="white"
        )
        self.capture_button.pack(pady=10)

        # Update camera preview
        self.update_camera()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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

    def on_close(self):
        """Stops the camera and closes the application."""
        self.picam.stop()
        self.root.destroy()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()