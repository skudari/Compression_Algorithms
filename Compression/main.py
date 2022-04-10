import sys
import numpy as np
import skimage.io
from matplotlib import pyplot as plt

if __name__ == '__main__':
    image = skimage.io.imread(fname="./Wavelet/Compressed_bin/compressed_wav_bior.jpeg")
    # tuple to select colors of each channel line
    colors = ("red", "green", "blue")
    channel_ids = (0, 1, 2)

    # create the histogram plot, with three lines, one for
    # each color
    plt.xlim([0, 256])
    for channel_id, c in zip(channel_ids, colors):
        histogram, bin_edges = np.histogram(
            image[:, :, channel_id], bins=256, range=(0, 256)
        )
        plt.plot(bin_edges[0:-1], histogram, color=c)

    plt.title("Wavelet Compressed Lenna Pixel Intensity Values")
    plt.xlabel("Color value")
    plt.ylabel("Pixels")

    plt.show()