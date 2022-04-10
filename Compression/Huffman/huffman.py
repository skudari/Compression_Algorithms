import cv2
import numpy as np
import time
import threading

from Huffman.tree import Tree

path_codes_r = dict()
path_codes_g = dict()
path_codes_b = dict()
nodes = [[], [], []]

def probability(channel):
    hist = dict()
    for i in range(0, np.size(channel, 0)):
        for j in range(0, np.size(channel, 1)):
            if hist.get(channel[i][j]) is not None:
                hist[channel[i][j]] += 1
            else:
                hist[channel[i][j]] = 1
    return hist


def encode_image(image):
    image_copy = image

    for i in range(0, np.size(image, 1)):
        for j in range(0, np.size(image, 2)):
            image_copy[0][i][j] = path_codes_r[image[0][i][j]]
            image_copy[1][i][j] = path_codes_g[image[1][i][j]]
            image_copy[2][i][j] = path_codes_b[image[2][i][j]]
    return image_copy


def encoding(node, rgb, path_code=""):
    # left - 0 , right - 1

    if node.left:
        a = encoding(node.left, rgb, path_code=path_code + "0")

    if node.right:
        a = encoding(node.right, rgb, path_code=path_code + "1")

    if not node.left and not node.right:
        node.code = path_code
        if rgb == "R":
            path_codes_r[node.value] = path_code
        elif rgb == "G":
            path_codes_g[node.value] = path_code
        elif rgb == "B":
            path_codes_b[node.value] = path_code
        else:
            print("NO RGB")
    return path_code


def get_sorted_nodes_list(nodes_list):
    return sorted(nodes_list, key=lambda x: x.prob)


def build_tree(channel, RGB):
    while len(channel) > 1:
        right_node = channel[1]
        left_node = channel[0]

        new_tree_node = Tree(left_node.prob + right_node.prob,
                             RGB,
                             value=str(right_node.value) + "," + str(left_node.value),
                             left=left_node,
                             right=right_node,
                             code=left_node.code + right_node.code)

        channel.remove(right_node)
        channel.remove(left_node)
        channel.append(new_tree_node)

        channel = get_sorted_nodes_list(channel)
    return channel

def encode_channel(original_img, channel, channel_symbol):
    dict = probability(original_img[:][:][channel])

    for symbol in dict.keys():
        # probability = Tree(red_dict.get(red))
        nodes[channel].append(Tree(dict.get(symbol),  channel_symbol, symbol))
    nodes[channel] = get_sorted_nodes_list(nodes[channel])

    tree = build_tree(nodes[channel], channel_symbol)
    encoding(tree[0], channel_symbol, "")


def huffman_encoding(original_img):
    #UNCOMMENT FOR NON-MULTITHREADING
    # encode_channel(original_img, 0, "R")
    # encode_channel(original_img, 1, "G")
    # encode_channel(original_img, 2, "B")

    t0 = threading.Thread(encode_channel(original_img, 0, "R"))
    t0.start()
    t1 = threading.Thread(encode_channel(original_img, 1, "G"))
    t1.start()
    t2 = threading.Thread(encode_channel(original_img, 2, "B"))
    t2.start()

    t0.join()
    t1.join()
    t2.join()

    encoded_image = encode_image(original_img)
    return encoded_image, [path_codes_r, path_codes_g, path_codes_b]


if __name__ == "__main__":
    filename = "/Users/skudari/Desktop/ECE 251 Compression/Images/Lenna.jpg"
    file_name = "Lenna"

    start = time.time()
    original_img = cv2.imread(filename)
    end_read = time.time()
    print("Read Time")
    print(end_read-start)

    encoding_startm= time.time()
    encoded_file, code_book = huffman_encoding(original_img)


    # length = 0
    # for i in range(0,np.shape(encoded_file)[0]):
    #     for j in range(0,np.shape(encoded_file)[1]):
    #         length += len(encoded_file[i][j])
    # print("Encoded Size:")
    # print(str(np.divide(length, 8)) + " bytes")

    encoding_end = time.time()
    print("encoding")
    print(encoding_end-encoding_startm)

    start_write = time.time()
    encoded_img = open("encoded_" + file_name + ".bin", "wb")
    encoded_img.write(encoded_file)
    end_write = time.time()
    print("writing")
    print(end_write - start_write)
