`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04.11.2025 17:24:37
// Design Name: 
// Module Name: uart_motor_control
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
// UART Based Motor Control for ZedBoard
// Controls motor direction and speed via UART commands
// Author: Manish Kumar (Modified by ChatGPT GPT-5)
//=======================================================

module uart_motor_control (
    input CLK,           // 100 MHz clock from ZedBoard
    input RST,           // Active high reset
    input RX,            // UART RX from USB-UART (FTDI)
    output [2:0] MOTOR   // MOTOR[0]=IN1, MOTOR[1]=IN2, MOTOR[2]=ENB(PWM)
);

    // UART wires
    wire [7:0] rx_data;
    wire rx_done;

    // Control bits: [2]=speed (0=low, 1=high), [1:0]=direction
    reg [2:0] control = 3'b000;

    // PWM parameters
    integer periodLength = 1000000;   // PWM period in clock cycles
    integer pulseLength1 = 200000;    // 20% duty (low speed)
    integer pulseLength2 = 900000;    // 90% duty (high speed)
    integer pulseLength = 0;
    integer counter = 0;

    // Instantiate UART Receiver (115200 baud @ 100 MHz)
    uart_rx #(.CLKS_PER_BIT(868)) uart_inst (
        .i_Clock(CLK),
        .i_Rx_Serial(RX),
        .o_Rx_DV(rx_done),
        .o_Rx_Byte(rx_data)
    );

    // PWM Counter
    always @(posedge CLK or posedge RST) begin
        if (RST)
            counter <= 0;
        else if (counter < periodLength)
            counter <= counter + 1;
        else
            counter <= 0;
    end

    // UART Command Decoder
    always @(posedge CLK or posedge RST) begin
        if (RST)
            control <= 3'b000;
        else if (rx_done) begin
            case (rx_data)
                "F": control <= 3'b001;   // Forward - high speed
                "f": control <= 3'b101;   // Forward - low speed
                "R": control <= 3'b110;   // Reverse - high speed
                "r": control <= 3'b010;   // Reverse - low speed
                "S": control <= 3'b000;   // Stop
                default: control <= 3'b000;
            endcase
        end
    end

    // Select PWM duty cycle based on speed bit
    always @(*) begin
        if (control[2] == 1'b0)
            pulseLength = pulseLength1;
        else
            pulseLength = pulseLength2;
    end

    // Assign motor outputs
    assign MOTOR[0] = control[0]; // IN1
    assign MOTOR[1] = control[1]; // IN2
    assign MOTOR[2] = (pulseLength > counter) ? 1'b1 : 1'b0; // ENB (PWM)

endmodule
