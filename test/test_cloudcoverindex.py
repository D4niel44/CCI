import cloudcoverindex.cloudcoverindex as cci
import pytest
from PIL import Image, ImageDraw


def test_mask_filter(subtests):
    """
    Test Partitions:
    Image Width: Greater than mask width, equal to Mask width
    Image Height: Greater than mask height, equal to Mask height
    Mask pixel values: 0, 255, in between
    """

    width = 100
    height = 100
    size = (width, height)

    # TestCase same size, mask pixels 0
    image = Image.new("RGB", size, (155, 155, 155))
    mask = Image.new("L", size, 0)
    with subtests.test(msg="Same Size, 0 transparency", image=image, mask=mask):
        result = cci.mask_filter(image, mask)
        assert_valid_composed_image(result, image, mask)

    # TestCase bigger width and height, mask pixels 255
    image = Image.new("RGB", (width + 100, height + 100), (0, 255, 0))
    mask = Image.new("L", size, 255)
    with subtests.test(msg="Bigger width and height, 255 transparency", image=image, mask=mask):
        central_rectangle = [50, 50, 150, 150]
        draw_rectangle(image, central_rectangle, (255, 0, 0))
        result = cci.mask_filter(image, mask)
        image = image.crop(central_rectangle)
        assert_valid_composed_image(result, image, mask)

    # TestCase bigger width, mask pixels in between
    image = Image.new("RGB", (width + 100, height), (0, 255, 0))
    mask = Image.new("L", size, 155)
    with subtests.test(msg="Bigger width, 155 transparency", image=image, mask=mask):
        central_rectangle = [50, 0, 150, height]
        draw_rectangle(image, central_rectangle, (255, 0, 0))
        result = cci.mask_filter(image, mask)
        image = image.crop(central_rectangle)
        assert_valid_composed_image(result, image, mask)

    # TestCase bigger height, mask pixels in between
    image = Image.new("RGB", (width, height + 100), (0, 255, 0))
    mask = Image.new("L", size, 50)
    with subtests.test(msg="Bigger width and height, 50 transparency", image=image, mask=mask):
        central_rectangle = [0, 50, width, 150]
        draw_rectangle(image, central_rectangle, (255, 0, 0))
        result = cci.mask_filter(image, mask)
        image = image.crop(central_rectangle)
        assert_valid_composed_image(result, image, mask)


def assert_valid_composed_image(result, original_rgb, original_alpha):
    assert result.mode == "RGBA"
    assert result.size == original_alpha.size

    result_pixels = result.load()
    original_rgb_pixels = original_rgb.load()
    original_alpha_pixels = original_alpha.load()
    for x in range(result.size[0]):
        for y in range(result.size[1]):
            assert equals_rgb_band(result_pixels[x, y], original_rgb_pixels[x, y])
            assert result_pixels[x, y][3] == original_alpha_pixels[x, y]


def equals_rgb_band(first, second):
    return first[0] == second[0] and first[1] == second[1] and first[2] == second[2]


def draw_rectangle(image, points, color):
    image = ImageDraw.Draw(image)
    image.rectangle(points, fill=color, outline=color)


def test_red_blue_filter(subtests):
    """
    Test Partitions for Red Blue Filter
    Input:
    - Red Component: 0, 255, in between
    - Blue Compontent 0, 255, in between
    - input image: all White, all Black
    - Transparency: transparent filters, not trnasparent filters
    Output:
    - All white, All black, Both
    """
    white_pixel = 255
    black_pixel = 0

    width = 100
    height = 100
    size = (width, height)

    # TestCase Red 0 Blue 255
    image = Image.new("RGBA", size, (0, 0, 255))
    with subtests.test(msg="Red 0 Blue 255", image=image):
        assert_color_all_pixels(image, size, black_pixel)

    # TestCase Red 255 Blue 0
    image = Image.new("RGBA", size, (255, 0, 0))
    with subtests.test(msg="Red 255 Blue 0", image=image):
        assert_color_all_pixels(image, size, white_pixel)

    # TestCase Only White pixels input
    image = Image.new("RGBA", size, (255, 255, 255))
    with subtests.test(msg="Only White pixels", image=image):
        assert_color_all_pixels(image, size, white_pixel)

    # TestCase Only black pixels
    image = Image.new("RGBA", size, (0, 0, 0))
    with subtests.test(msg="Only black pixels", image=image):
        assert_color_all_pixels(image, size, white_pixel)

    # TestCase Red/Blue > 0.95
    image = Image.new("RGBA", size, (200, 155, 100))
    with subtests.test(msg="Red/Blue > 0.95", image=image):
        assert_color_all_pixels(image, size, white_pixel)

    # TestCase Red/Blue < 0.95
    image = Image.new("RGBA", size, (99, 155, 135))
    with subtests.test(msg="Red/Blue < 0.95", image=image):
        assert_color_all_pixels(image, size, black_pixel)

    # TestCase Red/Blue > 0.95 Close to 0.95 value
    image = Image.new("RGBA", size, (100, 0, 104))
    with subtests.test(msg="R/B > 0.95 Close to 0.95", image=image):
        assert_color_all_pixels(image, size, white_pixel)

    # TestCase Red/Blue < 0.95 Close to 0.95 value
    image = Image.new("RGBA", size, (100, 0, 106))
    with subtests.test(msg="R/B < 0.95 Close to 0.95", image=image):
        assert_color_all_pixels(image, size, black_pixel)

    # TestCase Alpha channel of 0
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    with subtests.test(msg="Alpha Channel value 0", image=image):
        assert_color_all_pixels(image, size, black_pixel)


def assert_color_all_pixels(image, size, expected_pixel_value):
    res_pixels_map = cci.red_blue_filter(image).load()
    for x in range(size[0]):
        for y in range(size[1]):
            actual_pixel = res_pixels_map[x, y]
            if actual_pixel[1] == 0:
                # transparent pixels are ignored
                continue
            assert actual_pixel[0] == expected_pixel_value
