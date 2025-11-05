`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04.11.2025 14:28:25
// Design Name: 
// Module Name: uart_transmitter
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
module uart_transmitter #(
    parameter CLOCK_FREQ = 100_000_000,
    parameter BAUD_RATE = 115200
)(
    input clk,
    output reg tx_data,
    input [7:0] data_in,
    input data_valid
);

    localparam BIT_PERIOD = CLOCK_FREQ / BAUD_RATE;
    
    reg [3:0] state = 0;
    reg [15:0] counter = 0;
    reg [7:0] shift_reg = 0;
    reg [3:0] bit_index = 0;
    
    always @(posedge clk) begin
        case(state)
            0: begin // Idle state
                tx_data <= 1'b1;
                if (data_valid) begin
                    state <= 1;
                    shift_reg <= data_in;
                    counter <= BIT_PERIOD;
                    tx_data <= 1'b0; // Start bit
                    bit_index <= 0;
                end
            end
            1: begin // Send data bits
                if (counter == 0) begin
                    if (bit_index == 8) begin
                        state <= 2; // Stop bit
                        tx_data <= 1'b1;
                    end else begin
                        tx_data <= shift_reg[bit_index];
                        bit_index <= bit_index + 1;
                    end
                    counter <= BIT_PERIOD;
                end else begin
                    counter <= counter - 1;
                end
            end
            2: begin // Stop bit
                if (counter == 0) begin
                    state <= 0;
                end else begin
                    counter <= counter - 1;
                end
            end
        endcase
    end

endmodule