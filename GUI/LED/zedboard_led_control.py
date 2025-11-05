import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import time

# Check if pyserial is available
try:
    # First, let's check if there's a serial.py in current directory that's causing conflict
    current_dir_files = os.listdir('.')
    if 'serial.py' in current_dir_files:
        print("WARNING: Found 'serial.py' in current directory. This may conflict with pyserial.")
        print("Please rename or remove this file, or run the script from a different directory.")
    
    import serial
    import serial.tools.list_ports
    PYSERIAL_AVAILABLE = True
    print("✓ PySerial library loaded successfully")
except ImportError as e:
    print(f"✗ PySerial import error: {e}")
    PYSERIAL_AVAILABLE = False
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    PYSERIAL_AVAILABLE = False

class ZedBoardLEDControl:
    def __init__(self, root):
        self.root = root
        self.root.title("ZedBoard LED Controller")
        self.root.geometry("400x300")
        self.root.resizable(True, True)
        
        self.serial_connection = None
        self.connected_port = None
        
        self.setup_serial()
        self.create_gui()
        self.update_connection_status()
        
    def setup_serial(self):
        """Initialize serial connection"""
        if not PYSERIAL_AVAILABLE:
            print("Running in DEMO mode - PySerial not available")
            return
            
        try:
            # Get list of available ports
            available_ports = []
            ports = serial.tools.list_ports.comports()
            
            for port in ports:
                available_ports.append(port.device)
                print(f"Found port: {port.device} - {port.description}")
            
            if not available_ports:
                print("No serial ports found")
                return
                
            # Try to connect to common ZedBoard ports
            common_ports = ['COM3', 'COM4', 'COM5', 'COM6', 
                           '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
            
            for port in common_ports:
                if port in available_ports:
                    try:
                        print(f"Attempting to connect to {port}...")
                        self.serial_connection = serial.Serial(
                            port=port,
                            baudrate=115200,
                            timeout=1,
                            write_timeout=1
                        )
                        time.sleep(2)  # Wait for connection stabilization
                        self.connected_port = port
                        print(f"✓ Connected to {port}")
                        break
                    except Exception as e:
                        print(f"✗ Failed to connect to {port}: {e}")
                        continue
            
        except Exception as e:
            print(f"Serial setup error: {e}")
            self.serial_connection = None
    
    def create_gui(self):
        """Create the GUI layout"""
        # Main container
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_container, 
                               text="🎛️ ZedBoard LED Controller", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.LabelFrame(main_container, text="LED Controls", padding="15")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Control buttons
        self.btn_on = ttk.Button(control_frame, text="🔴 TURN ON", 
                                command=self.led_on, width=15)
        self.btn_on.grid(row=0, column=0, padx=10, pady=5)
        
        self.btn_off = ttk.Button(control_frame, text="⚪ TURN OFF", 
                                 command=self.led_off, width=15)
        self.btn_off.grid(row=0, column=1, padx=10, pady=5)
        
        self.btn_blink = ttk.Button(control_frame, text="✨ BLINK MODE", 
                                   command=self.led_blink, width=15)
        self.btn_blink.grid(row=0, column=2, padx=10, pady=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_container, text="Status", padding="15")
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Connection status
        self.connection_label = ttk.Label(status_frame, 
                                         text="Checking connection...",
                                         font=('Arial', 10))
        self.connection_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Command status
        self.command_label = ttk.Label(status_frame, 
                                      text="Ready to send commands",
                                      font=('Arial', 9))
        self.command_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Control buttons
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="🔄 Refresh Connection", 
                  command=self.refresh_connection).grid(row=0, column=0, padx=10)
        
        ttk.Button(button_frame, text="📋 Port Info", 
                  command=self.show_port_info).grid(row=0, column=1, padx=10)
        
        # Instructions
        instr_text = """Commands:
• '1' = Turn LED ON
• '0' = Turn LED OFF  
• '2' = Blink Mode

Make sure ZedBoard is connected via USB and programmed with the LED control firmware."""
        
        instr_label = ttk.Label(main_container, text=instr_text,
                               font=('Arial', 8), foreground="gray", justify=tk.LEFT)
        instr_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=10)
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def update_connection_status(self):
        """Update the connection status display"""
        if not PYSERIAL_AVAILABLE:
            status_text = "❌ PySerial not installed - Running in DEMO mode"
            status_color = "red"
        elif self.serial_connection and self.serial_connection.is_open:
            status_text = f"✅ Connected to {self.connected_port}"
            status_color = "green"
        else:
            status_text = "❌ Not connected to ZedBoard"
            status_color = "red"
        
        self.connection_label.config(text=status_text, foreground=status_color)
    
    def send_command(self, command, description):
        """Send command to ZedBoard"""
        if not PYSERIAL_AVAILABLE:
            self.command_label.config(text=f"DEMO: {description} (would send '{command}')", foreground="blue")
            return
            
        if not self.serial_connection or not self.serial_connection.is_open:
            self.command_label.config(text="❌ Not connected to ZedBoard", foreground="red")
            return
        
        try:
            # Send the command
            self.serial_connection.write(command.encode('utf-8'))
            self.command_label.config(text=f"✅ Sent: {description} ('{command}')", foreground="green")
            print(f"Sent command: '{command}' - {description}")
            
        except Exception as e:
            error_msg = f"❌ Error sending command: {str(e)}"
            self.command_label.config(text=error_msg, foreground="red")
            print(error_msg)
    
    def led_on(self):
        self.send_command('1', "LED ON")
    
    def led_off(self):
        self.send_command('0', "LED OFF")
    
    def led_blink(self):
        self.send_command('2', "BLINK MODE")
    
    def refresh_connection(self):
        """Refresh the serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        
        self.setup_serial()
        self.update_connection_status()
        self.command_label.config(text="Connection refreshed", foreground="orange")
    
    def show_port_info(self):
        """Show information about available serial ports"""
        if not PYSERIAL_AVAILABLE:
            messagebox.showwarning("PySerial Not Available", 
                                 "PySerial library is not installed.\n"
                                 "Please install it using: pip install pyserial")
            return
        
        try:
            ports = serial.tools.list_ports.comports()
            port_info = "Available Serial Ports:\n\n"
            
            if not ports:
                port_info += "No serial ports found!"
            else:
                for i, port in enumerate(ports):
                    port_info += f"{i+1}. {port.device}\n"
                    port_info += f"   Description: {port.description}\n"
                    port_info += f"   HWID: {port.hwid}\n\n"
            
            messagebox.showinfo("Serial Port Information", port_info)
        except Exception as e:
            messagebox.showerror("Error", f"Could not get port information: {e}")
    
    def __del__(self):
        """Cleanup when closing"""
        if hasattr(self, 'serial_connection') and self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial connection closed")

def main():
    """Main application entry point"""
    print("Starting ZedBoard LED Controller...")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    root = tk.Tk()
    app = ZedBoardLEDControl(root)
    
    def on_closing():
        """Handle application closing"""
        if hasattr(app, 'serial_connection') and app.serial_connection and app.serial_connection.is_open:
            app.serial_connection.close()
            print("Serial connection closed on exit")
        root.destroy()
        print("Application closed")
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Center the window
    root.eval('tk::PlaceWindow . center')
    
    print("GUI initialized successfully")
    print("=" * 50)
    
    root.mainloop()

if __name__ == "__main__":
    main()