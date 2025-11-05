`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04.11.2025 17:25:18
// Design Name: 
// Module Name: uart_rx
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

//=======================================================
// UART Receiver for 8N1 Format
// Supports 115200 baud @ 100 MHz clock
//=======================================================

module uart_rx
#(parameter CLKS_PER_BIT = 868)
(
    input i_Clock,
    input i_Rx_Serial,
    output reg o_Rx_DV,
    output reg [7:0] o_Rx_Byte
);

    parameter IDLE         = 3'b000;
    parameter RX_START_BIT = 3'b001;
    parameter RX_DATA_BITS = 3'b010;
    parameter RX_STOP_BIT  = 3'b011;
    parameter CLEANUP      = 3'b100;

    reg [2:0] r_SM_Main = 0;
    reg [9:0] r_Clock_Count = 0;
    reg [2:0] r_Bit_Index = 0;
    reg [7:0] r_Rx_Byte = 0;

    always @(posedge i_Clock) begin
        case (r_SM_Main)
            IDLE: begin
                o_Rx_DV <= 1'b0;
                if (i_Rx_Serial == 1'b0) begin
                    r_SM_Main <= RX_START_BIT;
                    r_Clock_Count <= 0;
                end
            end

            RX_START_BIT: begin
                if (r_Clock_Count == (CLKS_PER_BIT - 1)/2) begin
                    if (i_Rx_Serial == 1'b0) begin
                        r_Clock_Count <= 0;
                        r_SM_Main <= RX_DATA_BITS;
                        r_Bit_Index <= 0;
                    end else
                        r_SM_Main <= IDLE;
                end else
                    r_Clock_Count <= r_Clock_Count + 1;
            end

            RX_DATA_BITS: begin
                if (r_Clock_Count < CLKS_PER_BIT - 1)
                    r_Clock_Count <= r_Clock_Count + 1;
                else begin
                    r_Clock_Count <= 0;
                    r_Rx_Byte[r_Bit_Index] <= i_Rx_Serial;
                    if (r_Bit_Index < 7)
                        r_Bit_Index <= r_Bit_Index + 1;
                    else
                        r_SM_Main <= RX_STOP_BIT;
                end
            end

            RX_STOP_BIT: begin
                if (r_Clock_Count < CLKS_PER_BIT - 1)
                    r_Clock_Count <= r_Clock_Count + 1;
                else begin
                    o_Rx_Byte <= r_Rx_Byte;
                    o_Rx_DV <= 1'b1;
                    r_Clock_Count <= 0;
                    r_SM_Main <= CLEANUP;
                end
            end

            CLEANUP: begin
                r_SM_Main <= IDLE;
                o_Rx_DV <= 1'b0;
            end

            default: r_SM_Main <= IDLE;
        endcase
    end
endmodule
