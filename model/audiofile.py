from pathlib import Path
from utils.audio.audio_utils import calculate_simplified_rms
import numpy as np
import os

from utils.file_utils.load_audio_file import load_audio_file

class AudioFile():
    def __init__(self, full_path: Path|str):
        self.full_path = str(full_path)
        self.rel_name = os.path.basename(full_path)
        self.ok, self.n_channels, self.rate, self.bit_depth, self.channels_data = load_audio_file(full_path)
        self.n_samples = len(self.channels_data[0]) if self.channels_data else 0
        self.simplified = []
        self.only_filename = file_name = os.path.basename(full_path)
        
    def get_simplified(self, height: int, width: int):
        
        max__ = (2 ** self.bit_depth)/2
        
        if len(self.simplified) > 0:
            return self.simplified
        n_little_samples = 0
        
        
        for ch_data in self.channels_data:
            sub_res = calculate_simplified_rms(ch_data, chunk_size=100)
            n_little_samples = len(sub_res)
            sub_res = [(r*height)/max__ for r in sub_res]
            self.simplified.append(sub_res)
        
        self.simplified = [
            sum([self.simplified[ch_no][i] for ch_no in range(0, self.n_channels)])
            for i in range(0, n_little_samples)]
            
        return self.simplified