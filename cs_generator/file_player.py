from cs_generator.cs_model import CsdInstrument
from cs_generator.simple_instruments import GlobalTempPath, OscHandle, max_time


class FilePlayerInstr(CsdInstrument):
    def __init__(self, global_path: GlobalTempPath, **kwargs):
        super().__init__(**kwargs)
        self.body_str = f"""
        Spath strcpy {global_path.name}
        istarttime init p2
        iduration init p3
        ioffset init p4
        a_L, a_R diskin2 Spath, 1, ioffset;
        outs a_L, a_R
        """


class FilePlayerOscRecevier(CsdInstrument):
    def __init__(self, osc_handle:OscHandle, global_path: GlobalTempPath, **kwargs):
        super().__init__(**kwargs)
        self.global_variables.append(osc_handle)
        self.body_str = f"""
        kf1 init 0
        kino init 0
        kstart init 0.0
        kfdur init 0.1
        koffset init 0
        Spath init ""
        km  OSClisten {osc_handle.name}, "/playfile", "ifffs", kino, kstart, kfdur, koffset, Spath
        if (km != 0) then
            printks "Spath: %s\\n", 0, Spath
            {global_path.name} strcpyk Spath
            printks "gSpath: %s\\n", 0, {global_path.name}
            event "i", kino, kstart, kfdur, koffset
        endif
    """
        self.eternal_events = [{"p1":0, "p2":max_time}]