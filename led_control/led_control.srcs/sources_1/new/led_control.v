`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03.11.2025 17:44:47
// Design Name: 
// Module Name: led_control
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module top(
    input clk_100MHz,
    input uart_rx,           // J14 UART RX
    output [7:0] leds,       // ZedBoard LEDs
    output [7:0] debug_out   // For debugging
);

    wire led_control;
    
    uart_led_controller uart_led (
        .clk_100MHz(clk_100MHz),
        .uart_rx(uart_rx),
        .led_out(led_control),
        .debug_byte(debug_out)
    );
    
    // Connect to first LED
    assign leds[0] = led_control;
    assign leds[7:1] = 7'b0000000;  // Turn off other LEDs

endmodule