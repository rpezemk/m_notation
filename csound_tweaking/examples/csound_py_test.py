import os
import subprocess
import tempfile
from typing import Any

# general path of csd file generated (TODO generated)
path = "/tmp/n_file.csd"

def try_save_in_temp(content: str):
    global path
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        
    with open(path, 'w') as file:
        # Write the string to the file
        file.write(content)
    
def run_example():
    csd_file = "/home/przemek/n_commander/csound_tweaking/instruments/test_instrument.csd"
    with open(csd_file, 'r') as file:
        generated_content = file.read()
        try_save_in_temp(generated_content)
    process = subprocess.Popen(["csound", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

def run_example_2():
    csd_file = "/home/przemek/n_commander/csound_tweaking/instruments/test_instrument.csd"
    with open(csd_file, 'r') as file:
        generated_content = file.read()
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csd") as temp_file:
        temp_file.write(generated_content)
        temp_file_path = temp_file.name
        # Run Csound with the temporary file
        with open(temp_file_path, 'r') as file:
            a = file.read()
            print(a)
        subprocess.run(["csound", temp_file_path])
        # Clean up the temporary file
        os.unlink(temp_file_path)