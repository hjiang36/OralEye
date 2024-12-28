import tkinter as tk
import socket

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        ip_address = "No network"
    return ip_address

def show_ip():
    root = tk.Tk()
    root.title("IP Address")
    root.geometry("240x160")
    root.configure(bg="black")

    ip_address = get_ip_address()
    label = tk.Label(root, text=f"IP: {ip_address}", fg="white", bg="black", font=("Arial", 16))
    label.pack(expand=True)

    # Automatically close the window after 10 seconds
    root.after(10000, root.destroy)

    root.mainloop()

if __name__ == "__main__":
    show_ip()