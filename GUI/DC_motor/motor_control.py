import tkinter as tk
from tkinter import ttk
import serial
import time

# =============================
#  Configure your COM port
# =============================
# Example: Windows: 'COM3', Linux: '/dev/ttyUSB0'
FPGA_PORT = 'COM5'
BAUD_RATE = 115200

try:
    fpga = serial.Serial(FPGA_PORT, BAUD_RATE, timeout=1)
    print("✅ FPGA connected successfully on", FPGA_PORT)
except:
    print("❌ Could not connect to FPGA. Check COM port.")
    fpga = None

# =============================
#  GUI Functions
# =============================
def send_command(cmd):
    """Send a single ASCII command to FPGA"""
    if fpga:
        fpga.write(cmd.encode('utf-8'))
        print(f"Sent: {cmd}")

def set_speed(val):
    """Send speed value (0–255)"""
    if fpga:
        speed = int(float(val))
        fpga.write(bytes([speed]))
        print(f"Speed set to: {speed}")

# =============================
#  GUI Setup
# =============================
root = tk.Tk()
root.title("🌀 FPGA Motor Controller")
root.geometry("400x250")
root.resizable(False, False)

# Frame styling
frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Title
ttk.Label(frame, text="Motor Control Panel", font=("Arial", 16, "bold")).pack(pady=10)

# Buttons for direction
button_frame = ttk.Frame(frame)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="FORWARD", command=lambda: send_command('F')).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="REVERSE", command=lambda: send_command('R')).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="STOP", command=lambda: send_command('S')).grid(row=0, column=2, padx=10)

# Speed control slider
ttk.Label(frame, text="Speed Control (0–255)").pack(pady=5)
speed_slider = ttk.Scale(frame, from_=0, to=255, orient='horizontal', command=set_speed)
speed_slider.set(128)
speed_slider.pack(fill="x", padx=30)

# Exit button
ttk.Button(frame, text="Exit", command=root.destroy).pack(pady=10)

root.mainloop()

# Close serial when window closes
if fpga:
    fpga.close()
