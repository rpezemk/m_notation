from scipy.io import wavfile


import os
from pathlib import Path


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