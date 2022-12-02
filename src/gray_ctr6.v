/* Generated by Amaranth Yosys 0.10.0 (PyPI ver 0.10.0.dev47, git sha1 dca8fb54a) */

(* \amaranth.hierarchy  = "tucanae47_gray_ctr6" *)
(* top =  1  *)
(* generator = "Amaranth" *)
module tucanae47_gray_ctr6(io_in, io_out);
  reg \initial  = 0;
  wire [6:0] \$1 ;
  wire [6:0] \$2 ;
  wire [4:0] \$4 ;
  wire [7:0] \$6 ;
  wire clk;
  input [7:0] io_in;
  output [7:0] io_out;
  reg [5:0] o = 6'h00;
  reg [5:0] \o$next ;
  reg [5:0] q = 6'h00;
  reg [5:0] \q$next ;
  wire rst;
  assign \$2  = q + 1'h1;
  assign \$4  = q[5:1] ^ q[4:0];
  assign \$6  = + o;
  always @(posedge clk)
    o <= \o$next ;
  always @(posedge clk)
    q <= \q$next ;
  always @* begin
    if (\initial ) begin end
    \q$next  = \$2 [5:0];
    casez (rst)
      1'h1:
          \q$next  = 6'h00;
    endcase
  end
  always @* begin
    if (\initial ) begin end
    \o$next  = { q[5], \$4  };
    casez (rst)
      1'h1:
          \o$next  = 6'h00;
    endcase
  end
  assign \$1  = \$2 ;
  assign io_out = \$6 ;
  assign rst = io_in[1];
  assign clk = io_in[0];
endmodule

