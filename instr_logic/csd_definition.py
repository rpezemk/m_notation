from cs_generator.basic.exit_instr import ExitInstr, OscInstr, BeepInstr, TestInstr
from cs_generator.basic.templates import get_whole_body



def get_built_instrument():
    test = TestInstr().get_instr(1)
    ex = ExitInstr().get_instr(2)
    beep = BeepInstr().get_instr(7)
    osc = OscInstr().get_instr(1199)

    options = ["-odac"]

    runtime_data = [
            "sr = 44100",
            "ksmps = 32",
            "nchnls = 2",
            "0dbfs = 1",
    ]

    instruments = [test, ex, beep, osc]
    events = [
                "f 2 0 16384 10 1",
                "; i99077  0.01   7200  1        ; UDP OSC LISTENER",
                "i 1 0 20",
                "i 1199    0 20",
            ]

    res = get_whole_body(options, runtime_data, instruments, events)
    print(res)
    return res