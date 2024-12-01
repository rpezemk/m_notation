from typing import Callable
import threading

class WrappedJob():
    def __init__(self, job_func: Callable[[], None], mark_on_off: Callable[[bool], None] = None):
        self.is_running = False
        self.job_func = job_func
        pass

    def try_run(self):
        if not self.job_func or self.is_running:
            return
        
        t1 = threading.Thread(target=self.__inner_job__, args=[])
        t1.start()
        
    def __inner_job__(self):
        t1 = threading.Thread(target=self.job_func, args=[])
        t1.start()
        self.is_running = True
        t1.join()
        self.is_running = False