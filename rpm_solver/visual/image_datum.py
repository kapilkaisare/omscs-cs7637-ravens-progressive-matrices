from ..common.semantic_networks.node import Node
from ..common.logger import log
from itertools import product
from operator import itemgetter, add
from PIL import Image, ImageChops
import math

BLACK_PIXEL = (0, 0, 0, 255)
IDENTITY_THRESHOLD = 1000

class ImageDatum(Node):

    def __init__(self, datum, identifier):
        Node.__init__(self, datum)
        self.id = identifier
        self.image = None
        self.pixels = None
        self.black_pixels = None
        self.load_image()

    def __repr__(self):
        return '<ImageDatum ' + self.id + ' >'

    def __sub__(self, other):
        area = self.image.width * self.image.height
        difference = ImageChops.difference(self.image, other.image)
        sum_of_squares = reduce(add, map(lambda difference, i: difference*(i**2), difference, range(256)))
        return math.sqrt(sum_of_squares/area)


    def __eq__(self, other):
        return self.image - other.image <= IDENTITY_THRESHOLD

    def load_image(self):
        self.image =Image.open(self.datum.visualFilename)
        width, height = self.image.size
        self.pixels = self.image.load()
        self.black_pixels = [(x, y) for x, y in list(product(range(width), range(height))) if self.pixels[x, y] == BLACK_PIXEL]

    """
        compute_size - find the number of black pixels in image.
    """
    def compute_perceived_size(self):
        log("[ImageDatum/compute_perceived_size]")
        x_bounds = min(self.black_pixels, key=itemgetter(1))[1], max(self.black_pixels, key=itemgetter(1))[1]
        y_bounds = min(self.black_pixels)[0], max(self.black_pixels)[0]

        return (x_bounds[1] - x_bounds[0]) * (y_bounds[1] - y_bounds[0])

    def compute_fill_count(self):
        log("[ImageDatum/compute_fill_count]")
        return len(self.black_pixels)
