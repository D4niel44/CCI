from PIL import Image


# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

import cloudcoverindex.cloudcoverindex as cci

image1 = cci.CloudCoverApp("data/sample_images/11833.JPG", "data/mask-1350-sq.png")
image2 = cci.CloudCoverApp("data/sample_images/11836.JPG", "data/mask-1350-sq.png")
image3 = cci.CloudCoverApp("data/sample_images/11838.jpg", "data/mask-1350-sq.png")
image4 = cci.CloudCoverApp("data/sample_images/11839.JPG", "data/mask-1350-sq.png")
image5 = cci.CloudCoverApp("data/sample_images/11840.JPG", "data/mask-1350-sq.png")
image6 = cci.CloudCoverApp("data/sample_images/11841.JPG", "data/mask-1350-sq.png")

print("Image 1 Cloud Cover", image1.get_cloud_cover_index())
print("Image 2 Cloud Cover", image2.get_cloud_cover_index())
print("Image 3 Cloud Cover", image3.get_cloud_cover_index())
print("Image 4 Cloud Cover", image4.get_cloud_cover_index())
print("Image 5 Cloud Cover", image5.get_cloud_cover_index())
print("Image 6 Cloud Cover", image6.get_cloud_cover_index())
