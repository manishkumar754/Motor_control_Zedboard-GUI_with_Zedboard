import tkinter as tk
import serial
import serial.tools.list_ports

class ZedBoardLEDController:
    def __init__(self, root):
        self.root = root
        self.ser = None
        self.setup_gui()
        self.setup_serial()
    
    def setup_gui(self):
        self.root.title("ZedBoard LED Controller")
        self.root.geometry("300x200")
        self.root.configure(bg="#2b2b2b")
        
        # Title
        title = tk.Label(self.root, text="LED Control Panel", 
                        font=('Arial', 16, 'bold'), 
                        fg='white', bg='#2b2b2b')
        title.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="LED: OFF", 
                                   font=('Arial', 12), 
                                   fg='red', bg='#2b2b2b')
        self.status_label.pack(pady=5)
        
        # ON Button
        self.on_button = tk.Button(self.root, text="TURN LED ON", 
                                 font=('Arial', 12, 'bold'),
                                 command=self.led_on,
                                 bg='#4CAF50', fg='white',
                                 width=15, height=2)
        self.on_button.pack(pady=10)
        
        # OFF Button
        self.off_button = tk.Button(self.root, text="TURN LED OFF", 
                                  font=('Arial', 12, 'bold'),
                                  command=self.led_off,
                                  bg='#f44336', fg='white',
                                  width=15, height=2)
        self.off_button.pack(pady=10)
        
        # Serial status
        self.serial_label = tk.Label(self.root, text="", 
                                   font=('Arial', 10), 
                                   fg='yellow', bg='#2b2b2b')
        self.serial_label.pack(pady=5)
    
    def setup_serial(self):
        try:
            # Find and connect to ZedBoard serial port
            ports = list(serial.tools.list_ports.comports())
            for port in ports:
                if 'USB Serial' in port.description or 'ttyUSB' in port.device:
                    self.ser = serial.Serial(port.device, 115200, timeout=1)
                    self.serial_label.config(text=f"Connected: {port.device}")
                    print(f"Connected to {port.device}")
                    return
            
            # If automatic detection fails, try common ports
            for port in ['COM6', 'COM4', '/dev/ttyUSB0', '/dev/ttyUSB1']:
                try:
                    self.ser = serial.Serial(port, 115200, timeout=1)
                    self.serial_label.config(text=f"Connected: {port}")
                    print(f"Connected to {port}")
                    return
                except:
                    continue
                    
            self.serial_label.config(text="No serial port found")
            
        except Exception as e:
            self.serial_label.config(text=f"Error: {str(e)}")
    
    def led_on(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'1')
            self.status_label.config(text="LED: ON", fg='green')
            print("LED turned ON")
    
    def led_off(self):
        if self.ser and self.ser.is_open:
            self.ser.write(b'0')
            self.status_label.config(text="LED: OFF", fg='red')
            print("LED turned OFF")
    
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