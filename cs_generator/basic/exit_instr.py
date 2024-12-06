from cs_generator.model.cs_model import CsdInstrument, GlobalVariable

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

class OscPanic(CsdInstrument):
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
        self.eternal_events = [{"p1":0, "p2":7200}]
    
    

class OscMetro(CsdInstrument):
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
        self.eternal_events = [{"p1":0, "p2":7200}]
    
    
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
        outs 0.02*a1, 0.02*a1
        event_i "i", 2, 60, p3
        """
        
        self.eternal_events = [{"p1":0, "p2":20}, {"p1":99, "p2":2320}]