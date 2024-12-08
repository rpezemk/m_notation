from pathlib import Path
from scipy.io import wavfile
import os
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


def load_audio_file(full_path: Path|str) -> tuple[bool, int, int, int, list]:
    
    if not os.path.exists(full_path):
        return False, -1, -1, -1, []
    
    try:
        sample_rate, data = wavfile.read(full_path)
        n_channels = data.shape[1]
        bit_depth = data.dtype.itemsize * 8
        channels = []
        for idx in range(0, n_channels):
            channel_data = data[:, idx]
            channels.append(channel_data)
        return True, n_channels, sample_rate, bit_depth, channels
    
    except:
        return False, -1, -1, -1, []
