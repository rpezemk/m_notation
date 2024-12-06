import time
import threading
from typing import Callable, NoReturn, Tuple
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc import osc_server
from pythonosc import dispatcher
from pythonosc import udp_client
from pythonosc.osc_server import OSCUDPServer
import select
        
class MOscServer():
    def __init__(self, ip, port, handlers: list[(str, Callable)]):
        self.ip = ip
        self.port = port
        self.handlers = handlers
        self.server: OSCUDPServer = None
                
    def start_server(self) -> NoReturn:
        disp = dispatcher.Dispatcher()
        for handler in self.handlers:
            disp.map(*handler)  
        self.server = osc_server.ThreadingOSCUDPServer((self.ip, self.port), disp)
        self.server.timeout = 0.01
        sock = self.server.socket
        while True:
            ready_to_read, _, _ = select.select([sock], [], [], 0.1)  
            if ready_to_read:    
                self.server.handle_request()  
            time.sleep(0.11)  

    def gently_close(self):
        self.server.server_close()

def server_message_handler(address, *args):
    print(args)
    ...
    
msg_handlers = [("/*", server_message_handler)]
msg_handlers = [("/heartbeat", server_message_handler)]
m_osc_server = MOscServer("127.0.0.1", 8012, msg_handlers)

t1 = threading.Thread(target=m_osc_server.start_server, args=[])
print('defined "start"')
t1.start()
print('started')
print('(sleep 10)')
time.sleep(10)
t2 = threading.Thread(target=m_osc_server.gently_close, args=[])
print('gently stop')
t2.start()
print('stopped?')