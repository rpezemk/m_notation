from pythonosc.udp_client import SimpleUDPClient
import time

# OSC server details
ip = "127.0.0.1"
port = 8002       

client = SimpleUDPClient(ip, port)

# Send test OSC messages
try:
    for i in range(10):  
        kf1 = i * 0.1    
        kf2 = i * 0.2    
        client.send_message("/panic", []) 
        print(f"Sent: /panic [{kf1}]")
        time.sleep(0.5)  
except KeyboardInterrupt:
    print("Test interrupted by user.")
