import sys

from PIL import Image
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from cloudcoverindex.filters import mask_filter, red_blue_filter, convolution_filter

description = "Cloud Cover Index: Determine cloud cover index from jpeg image"
__version__ = "0.0.3"


class CloudCoverApp:

    def __init__(self, path, mask_path, downscale_factor=1):
        image = mask_filter(Image.open(path), Image.open(mask_path), downscale_factor=downscale_factor)
        image = red_blue_filter(image)
        image = convolution_filter(image)

        self.__image = image

    def get_cloud_cover_index(self):
        image_pixels = self.__image.load()
        width, height = self.__image.size
        total_pixels = 0
        cloud_pixels = 0
        for x in range(width):
            for y in range(height):
                l_band, a_band = image_pixels[x, y]
                if a_band == 0:
                    continue
                total_pixels += 1
                if l_band == 255:
                    cloud_pixels += 1
        return cloud_pixels / total_pixels

    def save(self, path):
        self.__image.save(path)


# TODO simplify main() implementation
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
                arguments.append(arg)  # should look into using Image.open(arg).verify() or maybe __init__(path) as well
        except:
            for char in arg:
                if char == 's' or char == 'S':
                    arguments.append('--S')

    args = parser.parse_args(arguments)
    if args.S:
        pass  # TODO Implement save(path)

    pass  # TODO Implement get_cloud_cover_index()


if __name__ == "__main__":
    main()
