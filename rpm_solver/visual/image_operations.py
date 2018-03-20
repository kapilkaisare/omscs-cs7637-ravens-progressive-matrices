from PIL import Image, ImageChops
from operator import add
import math

class ImageOperations(object):

    IDENTITY_THRESHOLD = 4.0

    @staticmethod
    def is_equal(image_a, image_b):
        return ImageOperations.minus(image_a, image_b) <= ImageOperations.IDENTITY_THRESHOLD

    @staticmethod
    def minus(image_a, image_b):
        diff = ImageChops.difference(image_a, image_b)
        h = diff.histogram()
        sq = (value*((idx%256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(image_a.size[0] * image_b.size[1]))
        # print "Differenmce >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        # print rms
        return rms

    @staticmethod
    def load_from_ravens_figure(ravens_figure):
        return Image.open(ravens_figure.visualFilename)

    @staticmethod
    def difference(image_a, image_b):
        return ImageChops.difference(image_a, image_b)