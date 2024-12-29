import tkinter as tk
import socket
from PIL import Image, ImageTk
from libcamera import CameraManager, Transform
import numpy as np

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address and Camera Preview")
        self.root.geometry("240x120")
        self.root.configure(bg="black")

        # Display IP Address
        ip_address = self.get_ip_address()
        self.label = tk.Label(root, text=f"IP: {ip_address}", fg="white", bg="black", font=("Arial", 10))
        self.label.pack(pady=10)

        # Create a canvas for the live camera feed
        self.canvas = tk.Canvas(root, width=640, height=360, bg="black")
        self.canvas.pack()

        # Initialize the camera
        self.manager = CameraManager()
        if not self.manager.cameras:
            self.label.config(text="No cameras available!")
            return

        self.camera = self.manager.cameras[0]
        self.camera.open()
        self.camera.configure(VideoConfig=(480, 360), transform=Transform.HFLIP)
        self.camera.start()

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
        request = self.camera.create_request()
        self.camera.queue_request(request)
        completed_request = self.camera.wait_for_request()
        if completed_request is not None:
            # Get frame data
            buffer = completed_request.buffers[0]
            width, height = buffer.metadata.size
            data = np.frombuffer(buffer.plane_data(), dtype=np.uint8)
            frame = data.reshape((height, width, 3))

            # Convert frame to ImageTk
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

        # Schedule the next frame update
        self.root.after(10, self.update_camera)

    def on_close(self):
        """Stops the camera and closes the application."""
        if self.camera:
            self.camera.stop()
            self.camera.close()
        self.root.destroy()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()