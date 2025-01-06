class GlobalVariable():
    def get_variable_def(self):
        ...


class BaseEvent():
    def __init__(self, p1_start, p2_duration):
        self.p1_start = p1_start
        self.p2_duration = p2_duration

    def for_instr_no(self, i_no):
        res_dict = {
            "p0":i_no,
            "p1":self.p1_start,
            "p2":self.p2_duration,
            }
        return res_dict

class CsdInstrument():
    def __init__(self, **kwargs):
        self.body_str = "\n"
        self.eternal_events:list[dict] = []
        self.global_variables:list[GlobalVariable] = []
        self.i_no = kwargs["i_no"]
        self.i_name = kwargs["i_name"]

    def get_instr(self, i_no: int):
        res = f"instr {i_no}"
        res += self.body_str
        res = res.strip()
        res += "\nendin"
        return res
