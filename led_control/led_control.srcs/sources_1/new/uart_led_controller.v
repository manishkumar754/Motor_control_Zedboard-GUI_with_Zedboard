`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03.11.2025 17:45:57
// Design Name: 
// Module Name: uart_led_controller
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

module uart_led_controller(
    input clk_100MHz,
    input uart_rx,           // J14 UART RX pin
    output reg led_out = 0,  // Initialize to 0
    output [7:0] debug_byte  // For debugging received data
);

    // UART Receiver parameters
    parameter CLK_FREQ = 100_000_000;  // 100 MHz
    parameter BAUD_RATE = 115200;
    parameter SAMPLE_COUNT = CLK_FREQ / BAUD_RATE;
    
    // UART receiver states
    localparam [2:0] 
        IDLE  = 3'b000,
        START = 3'b001,
        DATA  = 3'b010,
        STOP  = 3'b011;
    
    reg [2:0] state = IDLE;
    reg [15:0] counter = 0;
    reg [2:0] bit_index = 0;
    reg [7:0] rx_byte = 0;
    reg [7:0] received_data = 0;
    reg byte_received = 0;
    
    // Debug output
    assign debug_byte = received_data;
    
    // UART Receiver
    always @(posedge clk_100MHz) begin
        byte_received <= 1'b0;  // Explicit width
        
        case (state)
            IDLE: begin
                counter <= 0;
                bit_index <= 0;
                if (!uart_rx) begin  // Start bit detected (low)
                    state <= START;
                end
            end
            
            START: begin
                if (counter == (SAMPLE_COUNT/2)) begin
                    // Sample at middle of start bit
                    if (!uart_rx) begin
                        state <= DATA;
                        counter <= 0;
                    end else begin
                        state <= IDLE;
                    end
                end else begin
                    counter <= counter + 1;
                end
            end
            
            DATA: begin
                if (counter == SAMPLE_COUNT - 1) begin
                    rx_byte[bit_index] <= uart_rx;
                    counter <= 0;
                    if (bit_index == 3'd7) begin  // Explicit width
                        state <= STOP;
                    end else begin
                        bit_index <= bit_index + 1;
                    end
                end else begin
                    counter <= counter + 1;
                end
            end
            
            STOP: begin
                if (counter == SAMPLE_COUNT - 1) begin
                    received_data <= rx_byte;
                    byte_received <= 1'b1;
                    state <= IDLE;
                end else begin
                    counter <= counter + 1;
                end
            end
            
            default: state <= IDLE;
        endcase
    end
    
    // LED Control Logic
    always @(posedge clk_100MHz) begin
        if (byte_received) begin
            case (received_data)
                8'h31: led_out <= 1'b1;  // ASCII '1' - LED ON
                8'h30: led_out <= 1'b0;  // ASCII '0' - LED OFF
                8'h54: led_out <= ~led_out;  // ASCII 'T' - Toggle
                8'h74: led_out <= ~led_out;  // ASCII 't' - Toggle
                default: led_out <= led_out; // Maintain state
            endcase
        end
    end

endmodule