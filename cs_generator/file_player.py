from cs_generator.cs_model import CsdInstrument
from cs_generator.simple_instruments import GlobalTempPath, OscHandle, max_time


class FilePlayerInstr(CsdInstrument):
    def __init__(self, global_path: GlobalTempPath, **kwargs):
        super().__init__(**kwargs)
        self.body_str = f"""
        Spath strcpy {global_path.name}
        a_L, a_R diskin2 Spath, 1, p3;
        outs a_L, a_R    
        """


class FilePlayerOscRecevier(CsdInstrument):
    def __init__(self, osc_handle:OscHandle, global_path: GlobalTempPath, **kwargs):
        super().__init__(**kwargs)
        self.global_variables.append(osc_handle)
        self.body_str = f"""
        kf1 init 0
        kino init 0
        kfdur init 0.1
        koffset init 0
        Spath init ""
        km  OSClisten {osc_handle.name}, "/playfile", "iffs", kino, kfdur, koffset, Spath
        if (km != 0) then
            printks "Spath: %s\\n", 0, Spath
            {global_path.name} strcpyk Spath
            printks "gSpath: %s\\n", 0, {global_path.name}
            event "i", kino, 0, kfdur, koffset
        endif
    """
        self.eternal_events = [{"p1":0, "p2":max_time}]