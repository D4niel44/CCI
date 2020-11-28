#TODO add env python version control

import sys

from PIL import Image
from argparse import ArgumentParser, RawDescriptionHelpFormatter

description = "Cloud Cover Index: Determine cloud cover index from jpeg image"
__version__ = "0.0.1"

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

#TODO simplify main() implementation
def main():

    arguments = []
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{description} (Version: {__version__})")

    parser.add_argument("path", type=str,
                        metavar='PATH/TO/IMAGE', action="store",
                        help="read jpeg image and return cci")

    parser.add_argument("-s", "--S", action="store_true",
                        help="save greyscale output image (the dashes(-) are implied)")

    for arg in sys.argv[1:]:
        try:
            if arg == '-h' or arg == '--help' or Image.open(arg).format == 'JPEG':
                arguments.append(arg) #should look into using Image.open(arg).verify() or maybe __init__(path) as well
        except:
            for char in arg:
                if char == 's' or char == 'S':
                    arguments.append('--S')

    args = parser.parse_args(arguments)
    if args.S:
        pass #TODO Implement save(path)

    pass #TODO Implement get_cloud_cover_index()


if __name__ == "__main__":
    main()
