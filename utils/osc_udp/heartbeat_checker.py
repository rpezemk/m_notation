import threading
import time
from typing import Callable


class HeartbeatChecker():
    def __init__(self, period_s: float, logger_func: Callable[[bool], None] = None, report_state_changed_func: Callable[[bool], None] = None):
        self.period_s = period_s
        self.can_run = False
        self.history = [0, 0, 0]
        self.prev_history = [0, 0, 0]
        self.t1: threading.Thread = None
        self.hb_working = False
        self.flag = 0
        self.report_func = logger_func if logger_func is not None else lambda s: print(s)
        self.report_state_changed_func = report_state_changed_func if report_state_changed_func is not None else lambda s: ...
        self.report_state_changed_func(False)
        
    def start(self):
        self.can_run = True
        self.t1 = threading.Thread(target=self.bckg_check, args=[])
        self.t1.start()
        self.report_func('HeartbeatChecker started')
    
    def stop(self):
        self.can_run = False
        if self.t1.is_alive():
            self.t1.join(2)
        
    def are_same_lists(self, list1: list[int], list2: list[int]):
        are_same = len([1 for idx, k in enumerate(list1) if k == list2[idx]]) == len(list1) == len(list2)
        return are_same
        
    def bckg_check(self):
        while self.can_run:
            self.history = [self.history[1], self.history[2], self.flag]
            hb_working = not self.are_same_lists(self.history, self.prev_history)
            self.report_func(hb_working)
            if self.hb_working != hb_working:
                self.report_state_changed_func(hb_working)
            self.hb_working = hb_working
            self.prev_history = list(self.history)
            time.sleep(self.period_s)
    
    def is_ok(self):
        return len(set(self.history)) < len(self.history)
    
    def handle_flag(self, flag: int):
        self.flag = flag
        
def test_hb_checker():
    def change_state(hb: HeartbeatChecker):
        flag = 1
        cnt = 0
        while cnt < 10:
            hb.handle_flag(flag)
            time.sleep(1)
            flag = abs(1 - flag)
            cnt += 1
            
    print("should be True for 10s and False for next 10s, then finish")
    hb = HeartbeatChecker(0.5, None)
    t1 = threading.Thread(target=lambda: change_state(hb) , args=[])
    t1.start()
    hb.start()
    time.sleep(20)
    hb.stop()      
        
if __name__ == "__main__":
    test_hb_checker()        
        
