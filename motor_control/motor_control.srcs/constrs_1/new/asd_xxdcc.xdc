###################################################################
## CLOCK SOURCE (100 MHz clock on ZedBoard)
###################################################################
set_property PACKAGE_PIN Y9 [get_ports CLK]          ;# 100 MHz clock input
set_property IOSTANDARD LVCMOS33 [get_ports CLK]
create_clock -add -name sys_clk_pin -period 10.00 [get_ports CLK]
# 10 ns = 100 MHz

###################################################################
## UART INTERFACE (USB-UART J14)
###################################################################
set_property PACKAGE_PIN W12 [get_ports RX]          ;# UART RX (FTDI TX)
set_property IOSTANDARD LVCMOS33 [get_ports RX]

###################################################################
## MOTOR DRIVER INTERFACE (L293D / L298N)
## Using PMOD JA
###################################################################
# MOTOR[0] -> IN1 (Direction)
set_property PACKAGE_PIN Y10 [get_ports {MOTOR[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {MOTOR[0]}]

# MOTOR[1] -> IN2 (Direction)
set_property PACKAGE_PIN AA11 [get_ports {MOTOR[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {MOTOR[1]}]

# MOTOR[2] -> ENB (PWM)
set_property PACKAGE_PIN Y11 [get_ports {MOTOR[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {MOTOR[2]}]


###################################################################
## RESET (Push Button)
###################################################################
# Using BTNC (Center Button) as active-high reset
# You can also use BTNU/BTND if desired.
set_property PACKAGE_PIN P16 [get_ports RST]         ;# BTNC (Center pushbutton)
set_property IOSTANDARD LVCMOS33 [get_ports RST]