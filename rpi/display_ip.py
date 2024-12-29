import tkinter as tk
import socket
import cv2
from PIL import Image, ImageTk

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "No network"
    return ip_address

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Address and Camera Preview")
        self.root.geometry("240x120")
        self.root.configure(bg="black")

        # Display IP Address
        ip_address = get_ip_address()
        self.label = tk.Label(root, text=f"IP: {ip_address}", fg="white", bg="black", font=("Arial", 10))
        self.label.pack(pady=10)

        # Create a canvas for camera preview
        self.canvas = tk.Canvas(root, width=240, height=120)
        self.canvas.pack()

        # Open the camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.label.config(text="Camera not available")
        else:
            self.update_camera()

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB and create a PhotoImage for tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)

            # Display the image on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

            print("Camera updated...")

        # Call this function again after 10ms
        self.root.after(30, self.update_camera)

    def on_close(self):
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)  # Handle window close
    root.mainloop()