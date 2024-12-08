from cs_generator.cs_model import CsdInstrument, GlobalVariable

max_time = 7200 # two hours


class GlobalTempPath(GlobalVariable):
    def __init__(self, name):
        self.name = name
        
    def get_variable_def(self):
        res = f'{self.name} init "" ; '
        return res
class OscHandle(GlobalVariable):
    def __init__(self, port, name):
        self.port = port
        self.name = name
        
    def get_variable_def(self):
        res = f"{self.name} OSCinit {self.port}"
        return res


class ExitInstr(CsdInstrument):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.body_str = """
        exitnow;
        """


class OscPanicReceive(CsdInstrument):
    def __init__(self, osc_handle:OscHandle, panic_i_no, **kwargs):
        super().__init__(**kwargs)
        self.global_variables.append(osc_handle)
        self.body_str = f"""
        kk  OSClisten {osc_handle.name}, "/panic", ""
        if (kk != 0) then
            printks "QUITTING\\n", 0
            event "i", {panic_i_no}, 0, p3
        endif
    """
        self.eternal_events = [{"p1":0, "p2":max_time}]
    
    
class OscMetroReceive(CsdInstrument):
    def __init__(self, osc_handle:OscHandle, **kwargs):
        super().__init__(**kwargs)
        self.global_variables.append(osc_handle)
        self.body_str = f"""
        kf1 init 0
        kino init 0
        kfdur init 0.1

        km  OSClisten {osc_handle.name}, "/metro", "if", kino, kfdur
        if (km != 0) then
            printks "QUITTING\\n", 0
            event "i", kino, 0, kfdur
        endif
    """
        self.eternal_events = [{"p1":0, "p2":max_time}]
    
    
class BeepInstr(CsdInstrument):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.body_str = """
        a1 oscili 0.5, 4*440
        outs 0.1*a1, 0.1*a1
        """
        
class TestInstr(CsdInstrument):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.body_str = """
        a1 oscili 0.5, 440
        outs 0.07*a1, 0.07*a1
        event_i "i", 2, 60, p3
        """
        
        self.eternal_events = [{"p1":0, "p2":max_time}]
        
        
class CsHeartBeatToPy(CsdInstrument):
    def __init__(self, freq:int, port:int, **kwargs):
        super().__init__(**kwargs)
        self.freq = freq
        self.port = port
        
        self.body_str = f"""
            ktime init 0
            kvalue init 0
            ktrig metro {self.freq}
            kprevTrig init 0
            if ktrig == 1 && kprevTrig == 0 then
                kvalue = 1 - kvalue
            endif
            OSCsend kvalue, "", {self.port}, "/heartbeat", "i", kvalue
            kprevTrig = ktrig
        """
        
        self.eternal_events = [{"p1":0, "p2":max_time}]
        
        
class TapeNoiseInstr(CsdInstrument):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.body_str = f"""
            aNoise rand -1, 1           
            aOut = aNoise * 0.002
            outs aOut, aOut             
        """
        
        self.eternal_events = [{"p1":0, "p2":max_time}]

        

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
        
        
