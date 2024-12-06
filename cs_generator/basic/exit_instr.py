from cs_generator.model.cs_model import CsdInstrument



class ExitInstr(CsdInstrument):
    def __init__(self):
        self.body_str = """
        exitnow;
        """
        
        
class OscInstr(CsdInstrument):
    def __init__(self):
        self.body_str = """
        kf1 init 0
        kk  OSClisten gihandle, "/panic", ""
        if (kk != 0) then
            printks "QUITTING\\n", 0
            event "i", 2, 0, p3
        endif

        kino init 0
        kfdur init 0.1

        km  OSClisten gihandle, "/metro", "if", kino, kfdur
        if (km != 0) then
            printks "QUITTING\\n", 0
            event "i", kino, 0, kfdur
        endif
    """
    
class BeepInstr(CsdInstrument):
    def __init__(self):
        self.body_str = """
        a1 oscili 0.5, 4*440
        outs 0.1*a1, 0.1*a1
        """
        
class TestInstr(CsdInstrument):
    def __init__(self):
        self.body_str = """
        a1 oscili 0.5, 440
        outs 0.02*a1, 0.02*a1
        event_i "i", 2, 60, p3
        """