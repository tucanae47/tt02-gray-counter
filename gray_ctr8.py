from amaranth import *
from amaranth.cli import main


from amaranth.back import verilog
from amaranth.sim import Simulator

class Top(Elaboratable):
    def __init__(self):
        self.io_in = Signal(8)
        self.io_out = Signal(8)


    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.io_in.eq(self.io_in + 1)
        m.d.sync += self.io_out.eq(Cat(self.io_in[1:] ^ self.io_in[:7], self.io_in[-1]))
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
    ctr = Top()
    v = verilog.convert(
        ctr, name="tuc47_grayctr", ports=[ctr.io_out, ctr.io_in],
        emit_src=False, strip_internal_attrs=True)
    print(v)