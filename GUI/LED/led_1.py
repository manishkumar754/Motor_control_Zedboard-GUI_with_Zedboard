import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class ZedBoardLEDController:
    def __init__(self, root):
        self.root = root
        self.ser = None
        self.setup_gui()
        self.refresh_ports()
    
    def setup_gui(self):
        self.root.title("ZedBoard LED Controller - UART")
        self.root.geometry("400x300")
        self.root.configure(bg='#2b2b2b')
        
        # Title
        title = tk.Label(self.root, text="ZedBoard LED Control via UART", 
                        font=('Arial', 16, 'bold'), 
                        fg='white', bg='#2b2b2b')
        title.pack(pady=10)
        
        # Port Selection Frame
        port_frame = tk.Frame(self.root, bg='#2b2b2b')
        port_frame.pack(pady=10)
        
        tk.Label(port_frame, text="Select COM Port:", 
                font=('Arial', 10), fg='white', bg='#2b2b2b').pack(side=tk.LEFT)
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var, width=15)
        self.port_combo.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(port_frame, text="Refresh", 
                              command=self.refresh_ports,
                              bg='#2196F3', fg='white')
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        connect_btn = tk.Button(port_frame, text="Connect", 
                              command=self.connect_serial,
                              bg='#FF9800', fg='white')
        connect_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Disconnected", 
                                   font=('Arial', 12), 
                                   fg='red', bg='#2b2b2b')
        self.status_label.pack(pady=5)
        
        # LED Control Frame
        control_frame = tk.Frame(self.root, bg='#2b2b2b')
        control_frame.pack(pady=20)
        
        # ON Button
        self.on_button = tk.Button(control_frame, text="TURN LED ON", 
                                 font=('Arial', 12, 'bold'),
                                 command=self.led_on,
                                 bg='#4CAF50', fg='white',
                                 width=15, height=2, state=tk.DISABLED)
        self.on_button.pack(pady=10)
        
        # OFF Button
        self.off_button = tk.Button(control_frame, text="TURN LED OFF", 
                                  font=('Arial', 12, 'bold'),
                                  command=self.led_off,
                                  bg='#f44336', fg='white',
                                  width=15, height=2, state=tk.DISABLED)
        self.off_button.pack(pady=10)
        
        # Connection info
        self.info_label = tk.Label(self.root, text="Connect USB to J14 (PROG UART) on ZedBoard", 
                                 font=('Arial', 10), 
                                 fg='yellow', bg='#2b2b2b')
        self.info_label.pack(pady=10)
    
    def refresh_ports(self):
        """Refresh available serial ports"""
        ports = serial.tools.list_ports.comports()
        port_list = []
        for port in ports:
            port_list.append(f"{port.device} - {port.description}")
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.set(port_list[0])
    
    def connect_serial(self):
        """Connect to selected serial port"""
        if self.ser and self.ser.is_open:
            self.ser.close()
        
        try:
            port_str = self.port_var.get().split(' - ')[0]  # Extract just the port name
            self.ser = serial.Serial(port_str, 115200, timeout=1)
            self.status_label.config(text=f"Connected: {port_str}", fg='green')
            self.on_button.config(state=tk.NORMAL)
            self.off_button.config(state=tk.NORMAL)
            self.info_label.config(text="Connection successful! You can now control the LED.")
            print(f"Connected to {port_str}")
        except Exception as e:
            self.status_label.config(text=f"Connection failed: {str(e)}", fg='red')
            self.on_button.config(state=tk.DISABLED)
            self.off_button.config(state=tk.DISABLED)
    
    def led_on(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'1')
            self.info_label.config(text="LED command sent: ON")
            print("LED turned ON - Sent '1'")
    
    def led_off(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'0')
            self.info_label.config(text="LED command sent: OFF")
            print("LED turned OFF - Sent '0'")
    
    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZedBoardLEDController(root)
    
    def on_closing():
        app.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()