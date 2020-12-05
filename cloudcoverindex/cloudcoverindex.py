import sys

from PIL import Image
from argparse import ArgumentParser, RawDescriptionHelpFormatter


from cloudcoverindex.filters import mask_filter, red_blue_filter, convolution_filter

description = "Cloud Cover Index: Determine cloud cover index from jpeg image"
__version__ = "0.0.3"


class CloudCoverApp:
    """CloudCoverApp class that processes an image.
    It uses all filters and some methods from pillow
    to modify the image and extract it's cloud cover index.
    It also allows for the image to be saved.

    :param path: path to image file
    :type path: str
    :param mask_path: path to the mask image file
    :type mask_path: str
    :param path: path where the processed image is to be saved at
    :type path: str
    """
    
    def __init__(self, path, mask_path, downscale_factor=1):
        """Constructor method that applies all filters to an image and keeps it as an attribute.
        First the mask_filter is applied to reduce image size and
        decrease complexity, then the red_blue_filter to categorize
        the pixels of the image, and after the convolution filter
        is applied. Finally the image is kept.

        :param path: path to image file
        :type path: str
        :param mask_path: path to the mask image file
        :type mask_path: str
        """
        image = mask_filter(Image.open(path), Image.open(mask_path), downscale_factor=downscale_factor)
        image = red_blue_filter(image)
        image = convolution_filter(image)

        self.__image = image

    def get_cloud_cover_index(self):
        """Returns the value of the cloud cover index.
        The calculation is performed by counting every pixel that
        isn't transparent after the image has been processed by
        all filters. White pixels are counted as cloud pixels
        and divided by the total number of pixels in the image.

        :return: Cloud cover index
        :rtype: float
        """
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
        """Saves the image to a given path.
        Uses the pillow version of the same method.

        :param path: path where the processed image is to be saved at
        :type path: str
        """
        self.__image.save(path)


def main():
    arguments = []
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{description} (Version: {__version__})")

    parser.add_argument("paths", type=str, nargs='+',
                        metavar='PATH/TO/IMAGE', action="store",
                        help="read image(s) and return cloud cover index(es) (only jpeg images are supported)")

    parser.add_argument("-s", "--S", action="store_true",
                        help="save greyscale output image (the dashes(-) are implied)")

    parser.add_argument("-p", "--percentage", action="store_true",
                        help="return cloud cover index value as a percentage (the dashes(-) are implied)")

    for arg in sys.argv[1:]:
        try:
            if arg == '-h' or arg == '--help' or Image.open(arg).format == 'JPEG':
                arguments.append(arg)
        except:
            for char in arg:
                if char == 's' or char == 'S':
                    arguments.append('--S')
                if char == 'p':
                    arguments.append('--percentage')

    args = parser.parse_args(arguments)

    for path in args.paths:
        app = CloudCoverApp(path, "data/mask-1350-sq.png")

        image_name = ""
        image_path, image_format = path.rsplit('.',1)
        for char in reversed(image_path):
            if char == '/':
                break
            image_name = str(char) + image_name

        if args.S:
            app.save("data/saved_images/" + image_name + "-seg.png")
            print("Saved image named \"" + image_name + "-seg.png\" to data/saved_images/...")

        cloud_cover_index = app.get_cloud_cover_index()
        output = "Image named \"" + image_name + "\" has a Cloud Cover Index of "

        if args.percentage:
            output += str(100.0*cloud_cover_index)[:5] + " %"
        else:
            output += str(cloud_cover_index)

        print(output)


if __name__ == "__main__":
    main()
