from amaranth import *
from amaranth.cli import main


from amaranth.back import verilog
from amaranth.sim import Simulator

class Counter(Elaboratable):
    def __init__(self, width):
        self.v = Signal(width, reset=2**width-1)
        self.o = Signal(width)


    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.v.eq(self.v + 1)
        m.d.sync += self.o.eq(Cat(self.v[1:] ^ self.v[:3], self.v[-1]))
        return m

    def ports(self):
        return [self.v, self.o]


def test():
    """
    Testcase for GRAY_COUNTER generator.

    Run using `pytest gray_gc4.py`.
    """
    ctr = Counter(width=4)

    def testbench():
        # Trigger reset
        yield ctr.v.eq(0)
        # Collect 20 output bits
        out = []
        # yield
        for _ in range(200):
            yield
            # out.append((yield ctr.o))

    



    sim = Simulator(ctr)
    sim.add_clock(1/10e6)
    sim.add_sync_process(testbench)
    with sim.write_vcd("gc4.vcd", "gc4.gtkw", traces=ctr.ports()):
        sim.run()



if __name__ == "__main__":
    # Generate Verilog source for GC4.
    ctr = Counter(width=16)
    v = verilog.convert(
        ctr, name="tuc47_grayctr", ports=[ctr.v, ctr.o],
        emit_src=False, strip_internal_attrs=True)
    print(v)