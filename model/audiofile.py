from pathlib import Path
from scipy.io import wavfile

from utils.audio_utils import load_audio_file


class ChannelData():
    def __init__(self, data):
        self.data = data

class AudioFile():
    def __init__(self, full_path: Path|str):
        self.full_path = str(full_path)
        self.is_ok = False
        self.n_chan
        self.ok, self.n_channels, self.rate, self.bit_depth, self.data = load_audio_file(full_path)
        
    def get_simplified(self, half_height: int, width: int):
        test = self.data
        