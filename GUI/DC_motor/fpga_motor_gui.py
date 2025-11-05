import tkinter as tk
from tkinter import ttk
import serial

# 🛠 Configure your COM port here
fpga = serial.Serial('COM5', 115200, timeout=1)

def set_speed(val):
    speed = int(float(val))
    fpga.write(bytes([speed]))

def forward():
    fpga.write(b'F')

def reverse():
    fpga.write(b'R')

def stop():
    fpga.write(b'S')

# GUI setup
root = tk.Tk()
root.title("FPGA DC Motor Control")

tk.Label(root, text="FPGA Motor Controller", font=("Arial", 14, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Forward", width=10, command=forward).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Reverse", width=10, command=reverse).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Stop", width=10, command=stop).grid(row=0, column=2, padx=5)

tk.Label(root, text="Speed").pack(pady=5)
speed_slider = ttk.Scale(root, from_=0, to=255, orient="horizontal", command=set_speed)
speed_slider.set(128)
speed_slider.pack(fill="x", padx=20, pady=10)

root.mainloop()
