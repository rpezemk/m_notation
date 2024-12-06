from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

# Handler to process received OSC messages
def abc_channel_handler(unused_addr, args):
    print(f"Received value on /heartbeat: {args}")

# Setup the OSC server
ip = "127.0.0.1"  # Localhost (CSound sends OSC messages here)
port = 8012       # The port we are listening to (must match Csound's port)

dispatcher = Dispatcher()
dispatcher.map("/heartbeat", abc_channel_handler)

server = BlockingOSCUDPServer((ip, port), dispatcher)

# Start the server
print(f"Listening for OSC messages on {ip}:{port}")
server.serve_forever()
