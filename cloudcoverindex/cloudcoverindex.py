import sys

from PIL import Image, ImageFilter
from argparse import ArgumentParser, RawDescriptionHelpFormatter

description = "Cloud Cover Index: Determine cloud cover index from jpeg image(s)"
__version__ = "0.0.6"


def mask_filter(image, mask):
    """Applies a transparency mask to the given image.
    This method applies a transparency mask over an RGB
    image returning an RGBA image where its alpha channel
    are the values of the mask channel.
    Requires the mask to be a one channel image.
    :param image: A :class:`PIL.Image` image, must be in RGB mode. In case the image
    size is bigger than the mask size the the image is cropped to match the mask size.
    Note that the crop is done by removing the pixels in the corner, so the central pixels
    remains. If another kind of crop is needed should be done beforehand.
    :type image: class:`PIL.Image`
    :param mask: A :class:`PIL.Image` image, must have only one band/channel. Both the width and
    height of the mask must be smaller than width and height of the image.
    :type mask: class:`PIL.Image`
    :return: A :class:`PIL.Image` image in RGBA mode, keeping the original RGB
    values of the image and using the mask values for the alpha channel. The size of the returned
    image is the same as the size of the mask.
    :rtype: class:`PIL.Image`
    """
    if image is None:
        raise TypeError("Invalid None type argument")
    if mask is None:
        raise TypeError("Invalid None type argument")
    if mask.size[0] > image.size[0] or mask.size[1] > image.size[1]:
        raise ValueError("Both width and height of mask must be smaller than width and height of image")
    if image.mode != "RGB":
        raise ValueError("Only RGB images are supported")
    if len(mask.getbands()) != 1:
        raise ValueError("Mask must have only one channel")

    # Crop the image if bigger
    if image.size[0] > mask.size[0] or image.size[1] > mask.size[1]:
        image = __crop_borders(image, mask.size)

    return Image.merge("RGBA", image.split() + mask.split())


def __crop_borders(image, new_size):
    width = image.size[0]
    height = image.size[1]
    new_width = new_size[0]
    new_height = new_size[1]

    # Otherwise there is no point in calling this method
    assert width > new_width or height > new_height

    new_upper_left_corner = [(width - new_width) // 2, (height - new_height) // 2]
    new_lower_right_corner = [new_upper_left_corner[0] + new_width, new_upper_left_corner[1] + new_height]
    return image.crop(new_upper_left_corner + new_lower_right_corner)


def red_blue_filter(image):
    """Applies an R/B filter to each pixel in the image
    Applies a pixel wise filter to the provided image:
    Converts a pixel to white if the Red/Blue component ratio
    is bigger than 0.95, otherwise converts the pixel to black.
    For the pixel is transparent the resulting greyscale band value will be 0.
    Requires The image to be in RGBA mode.
    :param image: A :class:`PIL.Image` image.
    :type image: class:`PIL.Image`
    :return: A :class:`PIL.Image` LA image( greyscale with alpha channel).
    :rtype: class:`PIL.Image`
    """
    if image is None:
        raise TypeError("Invalid None type argument")
    if image.mode != "RGBA":
        raise ValueError("Only RGBA images are supported")

    width, height = image.size

    img_pixels = image.load()
    # Single band image for storing the computed filter values for each pixel
    greyscale_band = Image.new("L", image.size, color=0)
    greyscale_band_pixels = greyscale_band.load()
    for x in range(width):
        for y in range(height):
            greyscale_band_pixels[x, y] = __red_blue_pixel_filter(img_pixels[x, y])

    # Return the result of merging the computed greyscale image with the original alpha channel.
    return Image.merge("LA", (greyscale_band, image.split()[3]))


# TODO Try optimizing the method by precalculating this function for each 256*256 possible value
def __red_blue_pixel_filter(pixel):
    """This method applies the filter defined above to a pixel
    Returns an int value (255 or 0) as the result of applying the filter
    to the pixel. If the received pixel is transparent returns 0.
    """
    white_pixel = 255
    black_pixel = 0

    red_band_value = pixel[0]
    blue_band_value = pixel[2]
    alpha_band_value = pixel[3]

    if alpha_band_value == 0:  # transparent pixel case
        return black_pixel
    if blue_band_value == 0:  # 0 Blue component case
        return white_pixel
    if red_band_value / blue_band_value > 0.95:
        return white_pixel
    else:
        return black_pixel


def convolution_filter(image):
    """Applies a convolution filter to the provided image.
    The convolution filter is a simple mean 5x5 convolution filter but dividing the sum by 255.
    (Can be though of as counting every white pixel). Then the results are converted to binary (0, 255)
    values following the next rules.
    0 <= value <= 7 -> the returned pixel value is 0.
    7 < value <= 16 -> the returned pixel value doesnt change.
    16 < value <= 25 -> the returned pixel value is 255.
    Note that this filter is only applied to the L band of the image and in order to work properly
    the L band values must be either 0 or 255.
    Requires the image to be in mode LA.
    :param image: An Image in LA mode.
    :return: The image that results from applying the convolution filter described
    above to the provided image. The returned image contains two channels and the alpha channel
    remains unchanged from the original image.
    """
    if image.mode != "LA":
        raise ValueError("Only LA images allowed")

    # Initialize kernel
    kernel_size = (5, 5)
    kernel = [
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
    ]
    kernel_filter = ImageFilter.Kernel(kernel_size, kernel, scale=255)
    image_l_band, image_alpha_band = image.split()
    convolved_band = image_l_band.filter(kernel_filter)
    convolved_band = __select_output_pixels(image_l_band, convolved_band)
    return Image.merge("LA", (convolved_band, image_alpha_band))


def __select_output_pixels(original_band, convolved_band):
    original_pixels = original_band.load()
    convolved_pixels = convolved_band.load()

    width, height = original_band.size
    for x in range(width):
        for y in range(height):
            convolved_pixels[x, y] = __select_output_pixel(original_pixels[x, y], convolved_pixels[x, y])

    return convolved_band


def __select_output_pixel(original_pixel, convolved_pixel):
    black_pixel = 0
    white_pixel = 255

    if convolved_pixel <= 7:
        return black_pixel
    if convolved_pixel <= 16:
        return original_pixel
    return white_pixel


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

    def __init__(self, path, mask_path):
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
        image = mask_filter(Image.open(path), Image.open(mask_path))
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
