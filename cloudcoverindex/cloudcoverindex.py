# TODO add env python version control

import sys

from PIL import Image
from argparse import ArgumentParser, RawDescriptionHelpFormatter

description = "Cloud Cover Index: Determine cloud cover index from jpeg image"
__version__ = "0.0.0"


def mask_filter(image, mask):
    pass  # TODO Implement this method


def red_blue_filter(image):
    """Applies an RGB filter to each pixel in the image
    Applies a pixel wise filter to the provided image:
    Converts a pixel to white if the Red/Blue component ratio
    is bigger than 0.95, otherwise converts the pixel to black.
    Ignores transparent pixels.
    :param image: A :class:`PIL.Image` image.
    :type image: class:`PIL.Image`
    :return: A :class:`PIL.Image` image.
    :rtype: class:`PIL.Image
    """
    if image is None:
        raise ValueError("Invalid None argument")

    width, height = image.size

    img_pixels = image.load()
    for x in range(width):
        for y in range(height):
            img_pixels[x, y] = red_blue_pixel_filter(img_pixels[x, y])

    return image


# TODO Try optimizing the method by precalculating this function for each 256*256 possible value
def red_blue_pixel_filter(pixel):
    white_pixel = (255, 255, 255)
    black_pixel = (0, 0, 0)

    red_band_value = pixel[0]
    blue_band_value = pixel[2]
    alpha_band_value = pixel[3]

    if alpha_band_value == 0:  # transparent pixel case
        return pixel
    if blue_band_value == 0:  # 0 Blue component case
        return white_pixel
    if red_band_value / blue_band_value > 0.95:
        return white_pixel
    else:
        return black_pixel


def convolution_filter(image):
    pass  # TODO Implement this method


class CloudCoverApp:
    def __init__(self, path):
        pass  # TODO Implement this method

    def get_cloud_cover_index(self):
        pass  # TODO Implement this method

    def save(self, path):
        pass  # TODO Implement this method


def main():
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=f"{description} (Version: {__version__})")

    # TODO Implement this method
