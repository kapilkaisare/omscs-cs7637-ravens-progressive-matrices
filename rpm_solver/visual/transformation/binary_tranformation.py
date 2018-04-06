"""
Transformation
"""
from ... common.logger import log
from .transform import Transform, BLACK_PIXEL
from .transformation import Transformation, IMAGE_COMPOSITION_OPERATOR, IMAGE_COMPOSITION_OPERAND
from .image_operations import ImageOperations
from PIL import Image, ImageOps
from itertools import product

TRANSFORMS2x2 = [Transform.IDENTITY, Transform.MIRROR, Transform.FLIP, Transform.ROTATE_90, Transform.ROTATE_180, Transform.ROTATE_270, Transform.CENTER_FLOOD_FILL]

RMS_THRESHOLD = 94.0

class BinaryTransformation(Transformation):

    def __init__(self, tail, head, label):
        Transformation.__init__(self, tail, head, label)
        self.transforms = self.compute_transformations()

    def compute_transformations(self):
        transforms = []
        for transform in TRANSFORMS2x2:
            transformed_image = Transform.apply_transform(transform, self.tail.image)
            rms = ImageOperations.minus(self.head.image, transformed_image)
            print "---"
            print transform
            print rms
            if rms <= RMS_THRESHOLD:
                transforms.append((transform, rms))
        transforms.sort(key=lambda tup: tup[1])
        return transforms



