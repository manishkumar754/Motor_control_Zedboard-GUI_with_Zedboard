`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04.11.2025 14:26:12
// Design Name: 
// Module Name: led_blink
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


module led_blink(
    input clk,           // System clock (100MHz)
    input uart_rx,       // UART receive line
    output reg led_out,  // LED output
    output uart_tx       // UART transmit line (for debugging)
);

    // UART parameters
    parameter CLOCK_FREQ = 100_000_000;
    parameter BAUD_RATE = 115200;
    
    // UART receiver signals
    wire [7:0] uart_data;
    wire uart_data_valid;
    reg uart_data_ack = 0;
    
    // Command register
    reg [7:0] command = 8'h00;
    
    // Counter for blinking when in auto mode
    reg [31:0] counter = 0;
    parameter MAX_COUNT = 100_000_000; // 1 second blink
    
    // UART Receiver Instance
    uart_receiver #(
        .CLOCK_FREQ(CLOCK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) uart_rx_inst (
        .clk(clk),
        .rx_data(uart_rx),
        .data_out(uart_data),
        .data_valid(uart_data_valid)
    );
    
    // UART Transmitter Instance (optional - for debugging)
    uart_transmitter #(
        .CLOCK_FREQ(CLOCK_FREQ),
        .BAUD_RATE(BAUD_RATE)
    ) uart_tx_inst (
        .clk(clk),
        .tx_data(uart_tx),
        .data_in(8'h00), // Not used for now
        .data_valid(1'b0)
    );

    // Process UART commands
    always @(posedge clk) begin
        if (uart_data_valid) begin
            command <= uart_data; // Store the command
            
            // Echo back received command (optional)
            // You can implement echo functionality if needed
        end
    end
    
    // LED control logic based on command
    always @(posedge clk) begin
        case(command)
            8'h31: begin // ASCII '1' - Turn LED ON
                led_out <= 1'b1;
                counter <= 0;
            end
            8'h30: begin // ASCII '0' - Turn LED OFF
                led_out <= 1'b0;
                counter <= 0;
            end
            8'h32: begin // ASCII '2' - Blink mode
                if (counter == MAX_COUNT - 1) begin
                    counter <= 0;
                    led_out <= ~led_out;
                end else begin
                    counter <= counter + 1;
                end
            end
            default: begin // Default: maintain current state
                if (command == 8'h32) begin // If in blink mode, continue blinking
                    if (counter == MAX_COUNT - 1) begin
                        counter <= 0;
                        led_out <= ~led_out;
                    end else begin
                        counter <= counter + 1;
                    end
                end
                // Otherwise maintain current LED state
            end
        endcase
    end

endmodule