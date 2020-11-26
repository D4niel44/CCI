#TODO add env python version control

import sys

from PIL import Image
from argparse import ArgumentParser, RawDescriptionHelpFormatter

description = "Cloud Cover Index: Determine cloud cover index from jpeg image"
__version__ = "0.0.0"


def mask_filter(image, mask):
    pass  #TODO Implement this method


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
    pass  #TODO Implement this method


def convolution_filter(image):
    pass  #TODO Implement this method


class CloudCoverApp:
    def __init__(self, path):
        pass  #TODO Implement this method

    def get_cloud_cover_index(self):
        pass  #TODO Implement this method

    def save(self, path):
        pass  #TODO Implement this method


def main():

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=f"{description} (Version: {__version__})")

    #TODO Implement this method
