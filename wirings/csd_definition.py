from cs_generator.file_player import FilePlayerInstr, FilePlayerOscRecevier
from cs_generator.simple_instruments import GlobalTempPath, OscHandle, ExitInstr, TapeNoiseInstr, TestInstr, OscMetroReceive, CsdInstrument, BeepInstr, OscPanicReceive, CsHeartBeatToPy
from cs_generator.templates import get_whole_body
from wirings.csd_instr_numbers import panic_i_no, beep_i_no, py_to_cs_port, cs_to_py_port, file_play_instr_no

def get_built_instrument():
    osc_handle = OscHandle(py_to_cs_port, "gihandle")
    global_path = GlobalTempPath("gSpath")
    panic_instr = ExitInstr(i_no=panic_i_no, i_name="exit_instr")
    beep_instr = BeepInstr(i_no=beep_i_no, i_name="beep_instr")
    instruments: list[CsdInstrument] = [
        # TestInstr(i_no=1, i_name="test_instr"),
        beep_instr,
        panic_instr,
        OscMetroReceive(osc_handle, i_no=7, i_name="OSC_METRO"),
        OscPanicReceive(osc_handle, panic_i_no, i_no=9997, i_name="OSC_PANIC"),
        CsHeartBeatToPy(5, cs_to_py_port, i_no=9999, i_name="HEARTBEAT"),
        TapeNoiseInstr(i_no=12, i_name="TAPE_NOISE"),
        FilePlayerInstr(global_path, i_no=file_play_instr_no, i_name="FILE_PLAYER"),
        FilePlayerOscRecevier(osc_handle, global_path, i_no=15, i_name="FIRE_FILE_PLAY")
        ]
    options = ["-odac"]

    runtime_data = [
            "sr = 44100",
            "ksmps = 32",
            "nchnls = 2",
            "0dbfs = 1",
    ]

    events = [
        {
            "i_no":i.i_no,
            "i_name":i.i_name,
            "instr_events":i.eternal_events
        }
        for i_no, i in enumerate(instruments)
        if len(i.eternal_events) > 0]

    global_variables = [osc_handle, global_path]

    numbered_instruments = [{"i_no":i.i_no, "i_name":i.i_name, "body":i.body_str} for idx, i in enumerate(instruments)]

    res = get_whole_body(options, runtime_data, numbered_instruments, events, global_variables)
    # print(res)

    return res


