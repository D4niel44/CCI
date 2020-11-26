#TODO add env python version control

import sys

from PIL import Image
from argparse import ArgumentParser, RawDescriptionHelpFormatter

description = "Cloud Cover Index: Determine cloud cover index from jpeg image"
__version__ = "0.0.0"

def mask_filter(image, mask):
    pass #TODO Implement this method

def red_blue_filter(image):
    pass #TODO Implement this method

def convolution_filter(image):
    pass #TODO Implement this method

class CloudCoverApp:
    image

    def __init__(path):
        pass #TODO Implement this method

    def get_cloud_cover_index():
        pass #TODO Implement this method

    def save(path):
        pass #TODO Implement this method

def main():

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{description} (Version: {__version__})")
    
    #TODO Implement this method
