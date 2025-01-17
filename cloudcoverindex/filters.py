from PIL import Image, ImageFilter


def mask_filter(image, mask, downscale_factor=1):
    """Applies a transparency mask to the given image.
    This method applies a transparency mask over an RGB
    image returning an RGBA image where its alpha channel
    are the values of the mask channel.
    Requires the mask to be a one channel image.

    :param image: An image, must be in RGB mode. If image size is bigger than mask size the image is cropped
    :param mask: An image, must have only one band/channel. Width and height of mask must not exceed image dimensions
    :param downscale_factor: An optional factor to downscale the image.
    :type downscale_factor: int
    :return: An image in RGBA mode, keeping RGB values from image and adding mask as the A channel.
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
    if downscale_factor < 1:
        raise ValueError("Downscale factor must be grater than 1")

    # Crop the image if bigger
    if image.size[0] > mask.size[0] or image.size[1] > mask.size[1]:
        image = __crop_borders(image, mask.size)

    # Downscale both image and mask
    if downscale_factor != 1:
        image = image.resize((image.size[0] // downscale_factor, image.size[1] // downscale_factor), Image.LANCZOS)
        mask = mask.resize((mask.size[0] // downscale_factor, mask.size[1] // downscale_factor), Image.LANCZOS)

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

    :param image: An image.
    :return: An LA image( greyscale with alpha channel).
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


def __red_blue_pixel_filter(pixel):
    """This method applies the filter defined above to a pixel
    Returns an int value (255 or 0) as the result of applying the filter
    to teh pixel. If the received pixel is transparent returns 0.
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
    :return: An image. The returned image contains two channels and the alpha channel remains unchanged.
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
