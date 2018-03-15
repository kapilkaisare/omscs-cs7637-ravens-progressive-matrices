from ..common.semantic_networks.node import Node
from ..common.logger import log
from itertools import product
from operator import itemgetter
from PIL import Image

BLACK_PIXEL = (0, 0, 0, 255)

class ImageDatum(Node):

    def __init__(self, datum, identifier):
        Node.__init__(self, datum)
        self.id = identifier
        self.image = None
        self.pixels = None
        self.load_image()

    def __repr__(self):
        return '<ImageDatum ' + self.id + ' >'

    def load_image(self):
        self.image =Image.open(self.datum.visualFilename)
        self.pixels = self.image.load()

    """
        compute_size - find the number of black pixels in image.
    """
    def compute_perceived_size(self):
        log("[ImageDatum/compute_perceived_size]")
        width, height = self.image.size
        black_pixels = [(x, y) for x, y in list(product(range(width), range(height))) if self.pixels[x, y] == BLACK_PIXEL]
        x_bounds = min(black_pixels, key=itemgetter(1))[1], max(black_pixels, key=itemgetter(1))[1]
        y_bounds = min(black_pixels)[0], max(black_pixels)[0]

        return (x_bounds[1] - x_bounds[0]) * (y_bounds[1] - y_bounds[0])
