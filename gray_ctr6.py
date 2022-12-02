from amaranth import *
# import amaranth as am
from amaranth.cli import main


from amaranth.back import verilog
from amaranth.sim import Simulator

class Top(Elaboratable):
    def __init__(self):
        self.io_in = Signal(8)
        self.io_out = Signal(8)


    def elaborate(self, platform):
        m = Module()
        clk_in = self.io_in[0]
        rst_in = self.io_in[1]
        q = Signal(6)
        o = Signal(6)
        # Set up clock domain from io_in[0] and reset from io_in[1].
        cd_sync = ClockDomain("sync")
        m.d.comb += cd_sync.clk.eq(clk_in)
        m.d.comb += cd_sync.rst.eq(rst_in)
        m.domains += cd_sync
        
        m.d.sync += q.eq(self.io_in[2:])
        m.d.sync += q.eq(q + 1)
        m.d.sync += o.eq(Cat(q[1:] ^ q[:5], q[-1]))
        m.d.comb += self.io_out.eq(o)
        return m

    def ports(self):
        return [self.io_in, self.io_out]


def test():
    """
    Testcase for GRAY_COUNTER generator.

    Run using `pytest gray_gc4.py`.
    """
    ctr = Top()

    def testbench():
        yield ctr.io_in.eq(0)
        # Collect 22 output bits
        out = []
        yield
        for _ in range(22):
            out.append((yield ctr.io_out))
            yield
        assert out == [
            0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8,24,25,27,26,30,31]

    sim = Simulator(ctr)
    sim.add_clock(1/10e6)
    sim.add_sync_process(testbench)
    with sim.write_vcd("gc4.vcd", "gc4.gtkw", traces=ctr.ports()):
        sim.run()



if __name__ == "__main__":
    # Generate Verilog source for GC4.
    top = Top()
    v = verilog.convert(
        top, name="tucanae47_gray_ctr6", ports=[top.io_out, top.io_in],
        emit_src=False, strip_internal_attrs=True)
    print(v)