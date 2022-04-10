import time

import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from scipy import ndimage

# Order of Flip and Rotation
# 0: original
# 1: original, 90 degree rotation
# 2: original, 180 degree rotation
# 3: original, 270 degree rotation
# 4: flipped (left to right)
# 5: flipped, 90 degree rotation
# 6: flipped, 180 degree rotation
# 7: flipped, 270 degree rotation
from Wavelet.ThreadWithReturnValue import ThreadWithReturnValue

contrast = 0.75

class Encoder_Block:
    def __init__(self, img, original_size=(0, 0, 0), final_size=(0, 0, 0), step=0, factor=0):
        self.img = img
        self.size = np.shape(img)
        self.original_size = original_size
        self.final_size = final_size
        self.step = step
        self.factor = factor
        self.transforms = []

    def update_size(self):
        self.size = np.shape(self.img)

    def reduce(self):
        temp = np.zeros(
            (int(np.floor(np.divide(self.size[0], self.factor))), int(np.floor(np.divide(self.size[1], self.factor)))),
            dtype=float)

        for i in range(0, np.shape(temp)[0]):
            for j in range(0, np.shape(temp)[1]):
                temp[i, j] = np.mean(
                    self.img[i * self.factor:(i + 1) * self.factor, j * self.factor:(j + 1) * self.factor])

        self.img = temp
        self.size = np.shape(temp)
        return self

    def generate_transforms(self):
        transformed_blocks = []
        k_range = range(0, int(np.divide(np.subtract(self.size[0], self.final_size), self.step + 1)))
        l_range = range(0, int(np.divide(np.subtract(self.size[1], self.final_size), self.step + 1)))

        for k in k_range:
            for l in l_range:
                s_encoder_block = Encoder_Block(img=self.img[k * self.step:k * self.step + self.original_size,
                                                    l * self.step:l * self.step + self.original_size],
                                                original_size=self.original_size,
                                                final_size=self.final_size,
                                                step=self.step,
                                                factor=self.factor)
                s_encoder_block.reduce()
                transformed_blocks.append((k, l, s_encoder_block.transformations()))
        return transformed_blocks

    def compress(self):
        transformation_block = []
        transformed_blocks = self.generate_transforms()
        i_range = range(0, int(np.floor(np.divide(self.size[0], self.final_size))))
        j_range = range(0, int(np.floor(np.divide(self.size[1], self.final_size))))

        for i in i_range:
            transformation_block.append([])
            for j in j_range:
                min_d = float('inf')
                transformation_block[i].append(None)

                dest_block = self.img[i * self.final_size:(i + 1) * self.final_size,
                             j * self.final_size:(j + 1) * self.final_size]

                # for every transformation in the list of transformed blocks
                for k, l, t in transformed_blocks:
                    contrast_and_brightness = find_contrast_and_brightness_mine(dest_block, t)
                    for m in range(0, np.shape(contrast_and_brightness)[0]):
                        d = np.sum(np.square(
                            np.subtract(dest_block, contrast * t + contrast_and_brightness[m])))
                        #find the best transform
                        best_transform = True if d < min_d else False
                        if best_transform:
                            min_d = d
                            #k (x position of block), l(y position of block), index of transform, brightness -- contrast is a fixed variable
                            transformation_block[i][j] = (k, l, m, contrast_and_brightness[m])
        self.transforms = transformation_block
        return self.transforms

    def transformations(self):
        transforms = []
        region = self.img
        transforms.append(region)
        transforms.append(ndimage.rotate(region, 90, reshape=False))
        transforms.append(ndimage.rotate(region, 180, reshape=False))
        transforms.append(ndimage.rotate(region, 270, reshape=False))

        transforms.append(ndimage.rotate(region[::-1, :], 0, reshape=False))
        transforms.append(ndimage.rotate(transforms[4], 90, reshape=False))
        transforms.append(ndimage.rotate(transforms[4], 180, reshape=False))
        transforms.append(ndimage.rotate(transforms[4], 270, reshape=False))

        return np.array(transforms)


def get_position(index):
    if index == 0:
        return (0, 0)
    elif index == 1:
        return (0, 90)
    elif index == 2:
        return (0, 180)
    elif index == 3:
        return (0, 270)
    elif index == 4:
        return (1, 0)
    elif index == 5:
        return (1, 90)
    elif index == 6:
        return (1, 180)
    elif index == 7:
        return (1, 270)
    else:
        print("NOT A VALID INDEX")


def find_contrast_and_brightness_mine(D, S):
    global contrast
    bright = []
    for i in range(0, np.shape(S)[0]):
        brightness = (np.sum(D - contrast * S)) / D.size
        bright.append(brightness)
    return bright


def run_fractal_encode(img, original_size, final_size, factor, step):
    channel = Encoder_Block(img=img, original_size=original_size, final_size=final_size, factor=factor, step=step)
    channel.reduce()
    channel.compress()
    return channel


if __name__ == "__main__":
    factor = 8
    final_size = 4
    step = 8
    original_size = 8

    start = time.time()
    img = mpimg.imread('/Users/skudari/Desktop/ECE 251 Compression/Images/lena.gif')
    read = time.time()
    print("Read time")
    print(read-start)
    # red = Encoder_Block(img=img[:, :, 0], original_size=8, final_size=final_size, factor=factor, step=step)
    # green = Encoder_Block(img=img[:, :, 1], original_size=8, final_size=final_size, factor=factor, step=step)
    # blue = Encoder_Block(img=img[:, :, 2], original_size=8, final_size=final_size, factor=factor, step=step)
    #
    # red.reduce()
    # green.reduce()
    # blue.reduce()
    #
    # red.compress()
    # green.compress()
    # blue.compress()

    # img = np.concatenate((np.reshape(red.img, (red.size[0], red.size[1], 1)),
    #                       np.reshape(green.img, (green.size[0], green.size[1], 1)),
    #                       np.reshape(blue.img, (blue.size[0], blue.size[1], 1))), axis=2)
    encode_start = time.time()
    t0 = ThreadWithReturnValue(target=run_fractal_encode, args=(img[:, :, 0], original_size, final_size, factor, step,))
    t0.start()

    t1 = ThreadWithReturnValue(target=run_fractal_encode, args=(img[:, :, 1], original_size, final_size, factor, step,))
    t1.start()

    t2 = ThreadWithReturnValue(target=run_fractal_encode, args=(img[:, :, 2], original_size, final_size, factor, step,))
    t2.start()

    red = t0.join()
    green = t1.join()
    blue = t2.join()

    transformations = [red.transforms, green.transforms, blue.transforms]
    t = []
    for i in range(0, np.shape(transformations)[0]):
        for j in range(0, np.shape(transformations)[1]):
            for k in transformations[i][j]:
                t.append(k)
    encode_end = time.time()
    df = pd.DataFrame(t, columns=["k", "l", "flip and rotation", "brightness"])
    print("encode time")
    print(encode_end - encode_start)

    write_start = time.time()
    df.to_csv('fractal_encoded_known_index.csv')
    write_end = time.time()

    print("Write Time")
    print(write_end - write_start)
