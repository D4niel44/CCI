from PIL import Image


# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

import cloudcoverindex.cloudcoverindex as cci

image = Image.open("data/sample_images/11838.jpg")
mask = Image.open("data/mask-1350-sq.png")

# test with resizing
#mask = mask.resize((mask.size[0] // 4, mask.size[1] // 4), Image.LANCZOS)
#image = image.resize((image.size[0] // 4, image.size[1] // 4), Image.LANCZOS)

result = cci.mask_filter(image, mask)
result.show()
print(result.size)

result_after_filter = cci.red_blue_filter(result)
result_after_filter.show()
print(result_after_filter.size)
