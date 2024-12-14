import numpy as np
from scipy import stats
import sounddevice as sd

def list_audio_devices():
    devices = list(sd.query_devices())
    keys = ["index", "name", "default_samplerate", "max_input_channels", "max_output_channels"]
    res_dicts = []
    for dev in devices:
        new_dict = {}
        for k in keys:
            new_dict[k] = dev[k]
        res_dicts.append(new_dict)
        
    return res_dicts

def calculate_simplified_rms(samples, chunk_size=10):
    # Ensure that the samples array is a NumPy array
    samples = np.array(samples)

    # Compute the number of chunks
    n_chunks = len(samples) // chunk_size
    
    # Reshape the samples array into chunks
    chunks = samples[:n_chunks * chunk_size].reshape(-1, chunk_size)
    
    # Compute the maximum absolute value for each chunk
    max_abs = np.max(np.abs(chunks), axis=1)
    
    return max_abs.tolist()


