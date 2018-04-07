from PIL import Image, ImageChops
from operator import add
from itertools import product
import math

BLACK_PIXEL = (0, 0, 0, 255)
WHITE_PIXEL = (255, 255, 255, 255)

class ImageOperations(object):

    IDENTITY_THRESHOLD = 94.0

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
        return rms

    @staticmethod
    def calculate_minus(image_a, image_b):
        minus_image = Image.new("RGBA", image_a.size, "white")
        minus_image_pixels = minus_image.load()
        pixels_a = image_a.load()
        pixels_b = image_b.load()
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == BLACK_PIXEL and pixels_b[x, y] != BLACK_PIXEL:
                minus_image_pixels[x, y] = BLACK_PIXEL
        return minus_image

    @staticmethod
    def calculate_intersection(image_a, image_b):
        intersected_image = Image.new("RGBA", image_a.size, "white")
        intersected_image_pixels = intersected_image.load()
        pixels_a = image_a.load()
        pixels_b = image_b.load()
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == pixels_b[x, y] == BLACK_PIXEL:
                intersected_image_pixels[x, y] = BLACK_PIXEL
        return intersected_image

    @staticmethod
    def calculate_feature(image):
        width, height = image.size
        image_pixels = image.load()
        return len([(x, y) for x, y in list(product(range(width), range(height))) if image_pixels[x, y] == BLACK_PIXEL])

    @staticmethod
    def compute_similarity(image_a, image_b, alpha, beta):
        a_intersection_b = ImageOperations.calculate_intersection(image_a, image_b)
        a_minus_b = ImageOperations.calculate_minus(image_a, image_b)
        b_minus_a = ImageOperations.calculate_minus(image_a, image_b)
        f_a_intersection_b = float(ImageOperations.calculate_feature(a_intersection_b))
        f_a_minus_b = float(ImageOperations.calculate_feature(a_minus_b))
        f_b_minus_a = float(ImageOperations.calculate_feature(b_minus_a))
        return f_a_intersection_b/(f_a_intersection_b + (float(alpha) * f_a_minus_b) + (float(beta) * f_b_minus_a))

    @staticmethod
    def compute_similitude_fitness(image_a, image_b):
        a1b1 = ImageOperations.compute_similarity(image_a, image_b, 1, 1)
        a1b0 = ImageOperations.compute_similarity(image_a, image_b, 1, 0)
        a0b1 = ImageOperations.compute_similarity(image_a, image_b, 0, 1)

        if a1b1 > a1b0 and a1b1 > a0b1:
            fitness_score = a1b1
        elif a1b0 > a1b1 and a1b0 > a0b1:
            fitness_score = a1b0
        else:
            fitness_score = a0b1
        return fitness_score

    @staticmethod
    def load_from_ravens_figure(ravens_figure):
        return Image.open(ravens_figure.visualFilename)

    @staticmethod
    def difference(image_a, image_b):
        return ImageChops.difference(image_a, image_b)