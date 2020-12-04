from PIL import Image


# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

import cloudcoverindex.cloudcoverindex as cci

image = Image.open("data/sample_images/11840.JPG")
mask = Image.open("data/mask-1350-sq.png")

# test with resizing
mask = mask.resize((mask.size[0] // 8, mask.size[1] // 8), Image.LANCZOS)
image = image.resize((image.size[0] // 8, image.size[1] // 8), Image.LANCZOS)

result = cci.mask_filter(image, mask)
result_after_rb_filter = cci.red_blue_filter(result)
final_result = cci.convolution_filter(result_after_rb_filter)

