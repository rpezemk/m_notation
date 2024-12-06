from pythonosc.udp_client import SimpleUDPClient
import time
import os
import subprocess
from typing import Any

# OSC server details
ip = "127.0.0.1"
port = 8002       

client = SimpleUDPClient(ip, port)

# Send test OSC messages


# general path of csd file generated (TODO generated)
path = "/tmp/n_file.csd"

def try_save_in_temp(content: str):
    global path
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        
    with open(path, 'w') as file:
        # Write the string to the file
        file.write(content)
    
def start_CSOUND():
    csd_file = "./csound_tests/test_instrument.csd"
    with open(csd_file, 'r') as file:
        generated_content = file.read()
        try_save_in_temp(generated_content)
    process = subprocess.Popen(["csound", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


def quit_csound_nonsense():
    try:
        for i in range(10):  
            kf1 = i * 0.1    
            kf2 = i * 0.2    
            client.send_message("/panic", []) 
            print(f"Sent: /panic [{kf1}]")
            time.sleep(0.5)  
    except KeyboardInterrupt:
        print("Test interrupted by user.")
        
        
def quit_csound():
    try:
        client.send_message("/panic", []) 
    except KeyboardInterrupt:
        print("Something went wrong")


def beep():
    try:
        client.send_message("/metro", [7, 0.03]) 
    except KeyboardInterrupt:
        print("Something went wrong")
    

