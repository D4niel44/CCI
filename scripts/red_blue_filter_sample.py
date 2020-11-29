from PIL import Image


# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

import cloudcoverindex.cloudcoverindex as cci

image = Image.open("data/sample_images/11833.JPG").convert("RGBA")
image = cci.red_blue_filter(image)
image.show()
