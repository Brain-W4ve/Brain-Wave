import bioread
import numpy as np
from scipy.signal import medfilt


def apply_median_filter(file_content: bytes, kernel_size: int = 5):
    data = bioread.read(file_content)
    channel_data = data.channels[0].data
    return medfilt(channel_data, kernel_size)