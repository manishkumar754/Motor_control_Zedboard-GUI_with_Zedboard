## Clock signal
set_property PACKAGE_PIN Y9 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports clk]

## LED output
set_property PACKAGE_PIN Y11 [get_ports led_out] 
set_property IOSTANDARD LVCMOS33 [get_ports led_out]

## UART pins (using USB-UART bridge on ZedBoard)
set_property PACKAGE_PIN W12 [get_ports uart_rx]
set_property IOSTANDARD LVCMOS33 [get_ports uart_rx]

set_property PACKAGE_PIN W11 [get_ports uart_tx]
set_property IOSTANDARD LVCMOS33 [get_ports uart_tx]