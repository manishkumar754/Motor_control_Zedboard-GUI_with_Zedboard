`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04.11.2025 14:27:12
// Design Name: 
// Module Name: uart_receiver
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
module uart_receiver #(
    parameter CLOCK_FREQ = 100_000_000,
    parameter BAUD_RATE = 115200
)(
    input clk,
    input rx_data,
    output reg [7:0] data_out,
    output reg data_valid
);

    localparam BIT_PERIOD = CLOCK_FREQ / BAUD_RATE;
    
    reg [3:0] state = 0;
    reg [15:0] counter = 0;
    reg [7:0] shift_reg = 0;
    reg [3:0] bit_index = 0;
    
    always @(posedge clk) begin
        case(state)
            0: begin // Idle state
                data_valid <= 1'b0;
                if (rx_data == 1'b0) begin // Start bit detected
                    state <= 1;
                    counter <= BIT_PERIOD / 2;
                    bit_index <= 0;
                end
            end
            1: begin // Wait half bit period to sample in middle of bit
                if (counter == 0) begin
                    state <= 2;
                    counter <= BIT_PERIOD;
                end else begin
                    counter <= counter - 1;
                end
            end
            2: begin // Sample data bits
                if (counter == 0) begin
                    if (bit_index == 8) begin
                        state <= 3; // Stop bit
                        data_out <= shift_reg;
                        data_valid <= 1'b1;
                    end else begin
                        shift_reg[bit_index] <= rx_data;
                        bit_index <= bit_index + 1;
                        counter <= BIT_PERIOD;
                    end
                end else begin
                    counter <= counter - 1;
                end
            end
            3: begin // Stop bit and cleanup
                data_valid <= 1'b0;
                state <= 0;
            end
        endcase
    end

endmodule