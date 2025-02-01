from pythonosc.udp_client import SimpleUDPClient
import time
import os
import subprocess
from typing import Any
import tempfile

from wirings.csd_definition import get_built_instrument
from wirings.csd_instr_numbers import panic_i_no, beep_i_no, py_to_cs_port, local_ip, file_play_instr_no

# OSC server details
port = py_to_cs_port

client = SimpleUDPClient(local_ip, port)

# general path of csd file generated (TODO generated)
linux_path = "/tmp/n_file.csd"
windows_path = ""


# Create a temporary file


# The file persists after closing because delete=False
path = ""

def try_save_in_temp(content: str):
    # global linux_path
    # global windows_path
    # path = linux_path if os.name == 'posix' else (windows_path if os.name == 'nt' else ...) 
    # if os.path.exists(path) and os.path.isfile(path):
    #     os.remove(path)
    global path
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        path = tmp_file.name
        print(f"Temporary file created: {tmp_file.name}")
        
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path) 
    
    with open(path, 'w') as file:
        print('saving content to:')
        print(f"{path}")
        # Write the string to the file
        file.write(content)
    print(f"file: {path} written")
        
def start_CSOUND():
    csd_file = "./generated_instrument/autogenerated.csd"
    with open(csd_file, 'r') as file:
        generated_content = file.read()
        try_save_in_temp(generated_content)
    proc_args = ["C:\\Program Files\\Csound6_x64\\bin\\csound.exe", path]
    print(proc_args)
    process = subprocess.Popen(proc_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


def quit_csound():
    try:
        client.send_message("/panic", [])
    except:
        print("Something went wrong")


def play_ding():
    try:
        client.send_message("/metro", [beep_i_no, 0.03])
    except:
        print("Something went wrong")



def static_play_file():
    try:
        client.send_message("/playfile", [file_play_instr_no, 0, 10, 0.0, "/home/przemek/m_notation/audio_samples/harvard.wav"])
    except:
        print("Something went wrong")

def play_file(path: str):
    try:
        client.send_message("/playfile", [file_play_instr_no, 0, 10, 0.0, path])
    except:
        print("Something went wrong")

def save_file():
    content = get_built_instrument()
    current_dir = os.getcwd()
    relative = "./generated_instrument/autogenerated.csd"
    file_path = os.path.join(current_dir, relative)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(content)