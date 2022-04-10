import time

import cv2
import numpy as np
import pywt

from Huffman.huffman import huffman_encoding
from Wavelet.ThreadWithReturnValue import ThreadWithReturnValue


def get_coefficients(channel, wavelet):
    size = np.shape(channel)
    np.reshape(channel, (size[0], size[1], 1))
    coeffs = pywt.dwt2(channel, wavelet)
    return coeffs


def get_coeff_blocks(channel):
    return np.array(channel[0])
    # np.array(channel[1][0]), np.array(channel[1][1]), np.array(channel[1][2])


def div_by_max(channel, max_val):
    r, c = np.shape(channel)

    for i in range(0, r):
        for j in range(0, c):
            channel[i][j] = int((channel[i][j] / max_val) * 100.0)
    return channel


def run_wavelet_funct(channel, wavelet):
    coeff = get_coefficients(channel, wavelet)
    LL = get_coeff_blocks(coeff)
    # reconstruct image with Lowpass
    LL = div_by_max(LL, np.amax(LL))
    return LL


if __name__ == "__main__":
    print("ReadTime")
    start = time.time()
    img = cv2.imread("../Images/Lenna.jpg")
    end_read = time.time()
    print(end_read - start)

    start_encoding = time.time()
    # r_coeff = get_coefficients(img[:, :, 0], 'haar')
    # g_coeff = get_coefficients(img[:, :, 1], 'haar')
    # b_coeff = get_coefficients(img[:, :, 2], 'haar')
    #
    # LL_red = get_coeff_blocks(r_coeff)
    # LL_green = get_coeff_blocks(r_coeff)
    # LL_blue = get_coeff_blocks(r_coeff)
    #
    # # reconstruct image
    # R = div_by_max(LL_red, np.amax(LL_red))
    # G = div_by_max(LL_green, np.amax(LL_green))
    # B = div_by_max(LL_blue, np.amax(LL_blue))

    t_r = ThreadWithReturnValue(target=run_wavelet_funct, args=(img[:, :, 0], 'bior3.5',))
    t_g = ThreadWithReturnValue(target=run_wavelet_funct, args=(img[:, :, 1], 'bior3.5',))
    t_b = ThreadWithReturnValue(target=run_wavelet_funct, args=(img[:, :, 2], 'bior3.5',))

    t_r.start()
    t_g.start()
    t_b.start()

    R = t_r.join()
    G = t_g.join()
    B = t_b.join()

    width, height = np.shape(R)
    compressed_img = np.zeros((width, height, 3))

    compressed_img[:, :, 0] = R
    compressed_img[:, :, 1] = G
    compressed_img[:, :, 2] = B

    cv2.imwrite("Compressed_bin/compressed_wav_db.jpeg", np.array(compressed_img))

    img = cv2.imread("Compressed_bin/compressed_wav_db.jpeg")
    end_encoding = time.time()
    print("Encoding time")
    print(end_encoding-start_encoding)

    write_start = time.time()
    encoded_file, code_book = huffman_encoding(img)
    encoded_img = open("encoded" + "compressed_db" + ".bin", "wb")
    encoded_img.write(encoded_file)
    end_time = time.time()
    print("Write Time")
    print(end_time - write_start)
