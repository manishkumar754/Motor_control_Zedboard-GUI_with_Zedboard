import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time

# ======================================================
#  Function: Auto-detect FPGA COM port
# ======================================================
def find_fpga_port(baud=115200, timeout=0.1):
    """Scan all COM ports and return the one that connects successfully."""
    ports = list(serial.tools.list_ports.comports())
    print("🔍 Scanning available COM ports...")
    
    for port in ports:
        print(f"  Trying {port.device} ...")
        try:
            fpga = serial.Serial(port.device, baud, timeout=timeout)
            time.sleep(0.2)
            if fpga.is_open:
                print(f"✅ Connected to FPGA on {port.device}")
                return fpga
        except Exception as e:
            print(f"❌ {port.device} not responding ({e})")
    print("⚠️ No FPGA found. Please check connections.")
    return None

# ======================================================
#  Try to connect automatically
# ======================================================
fpga = find_fpga_port()

# ======================================================
#  GUI Control Functions
# ======================================================
def send_command(cmd):
    if fpga:
        fpga.write(cmd.encode('utf-8'))
        print(f"➡ Sent: {cmd}")
    else:
        messagebox.showerror("Connection Error", "FPGA not connected!")

def set_speed(val):
    if fpga:
        speed = int(float(val))
        fpga.write(bytes([speed]))
        print(f"⚙️ Speed set to: {speed}")
    else:
        messagebox.showerror("Connection Error", "FPGA not connected!")

# ======================================================
#  GUI Setup
# ======================================================
root = tk.Tk()
root.title("🌀 FPGA Motor Controller")
root.geometry("400x280")
root.resizable(False, False)

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Motor Control Panel", font=("Arial", 16, "bold")).pack(pady=10)

# FPGA connection status
status_label = ttk.Label(frame, text="", font=("Arial", 10))
status_label.pack(pady=5)

if fpga:
    status_label.config(text=f"✅ Connected to {fpga.port}", foreground="green")
else:
    status_label.config(text="❌ FPGA not connected", foreground="red")

# Control buttons
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
ttk.Button(frame, text="Exit", command=root.destroy).pack(pady=15)

root.mainloop()

# Close serial on exit
if fpga:
    fpga.close()
    print("🔌 FPGA connection closed.")
