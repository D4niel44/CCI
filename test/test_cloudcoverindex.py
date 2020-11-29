import cloudcoverindex.cloudcoverindex as cci
import pytest
from PIL import Image


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
    # TODO Create transparency test cases if using it
    width = 100
    height = 100
    size = (width, height)

    # TestCase Red 0 Blue 255
    image = Image.new("RGBA", size, (0, 0, 255))
    with subtests.test(msg="Red 0 Blue 255", image=image):
        assert_color_all_pixels(image, size, (0, 0, 0))

    # TestCase Red 255 Blue 0
    image = Image.new("RGBA", size, (255, 0, 0))
    with subtests.test(msg="Red 255 Blue 0", image=image):
        assert_color_all_pixels(image, size, (255, 255, 255))

    # TestCase Only White pixels input
    image = Image.new("RGBA", size, (255, 255, 255))
    with subtests.test(msg="Only White pixels", image=image):
        assert_color_all_pixels(image, size, (255, 255, 255))

    # TestCase Only black pixels
    image = Image.new("RGBA", size, (0, 0, 0))
    with subtests.test(msg="Only black pixels", image=image):
        assert_color_all_pixels(image, size, (255, 255, 255))

    # TestCase Red/Blue > 0.95
    image = Image.new("RGBA", size, (200, 155, 100))
    with subtests.test(msg="Red/Blue > 0.95", image=image):
        assert_color_all_pixels(image, size, (255, 255, 255))

    # TestCase Red/Blue < 0.95
    image = Image.new("RGBA", size, (99, 155, 135))
    with subtests.test(msg="Red/Blue < 0.95", image=image):
        assert_color_all_pixels(image, size, (0, 0, 0))


def assert_color_all_pixels(image, size, color):
    res_pixels_map = cci.red_blue_filter(image).load()
    for x in range(size[0]):
        for y in range(size[1]):
            assert res_pixels_map[x, y] == color
