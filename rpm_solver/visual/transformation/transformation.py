"""
Transformation
"""
from ... common.logger import log
from ... common.semantic_networks.link import Link
from .transform import Transform
from .image_operations import ImageOperations
from PIL import Image, ImageOps
from itertools import product

class IMAGE_COMPOSITION_OPERATOR(object):
    NONE = "None"
    ADDITION = "addition"
    SUBTRACTION = "subtraction"

class IMAGE_COMPOSITION_OPERAND(object):
    NONE = "None"
    A_MINUS_B = "a_minus_b"
    B_MINUS_A = "b_minus_a"

BLACK_PIXEL = (0, 0, 0, 255)

class Transformation(Link):

    def __init__(self, tail, head, label):
        Link.__init__(self, tail, head, label)
        self.id = self.label.value




