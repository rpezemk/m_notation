class CscOrchestra():
    def __init__(self):
        pass

        
class CsdScores():
    def __init__(self):
        pass


class CsdWhole():
    def __init__(self):
        self.scores
    
class CsdInstrument():
    def __init__(self):
        self.body_str = "\n"
        
    def get_instr(self, i_no: int):
        res = f"instr {i_no}"
        res += self.body_str
        res = res.strip()
        res += "\nendin"
        return res
    