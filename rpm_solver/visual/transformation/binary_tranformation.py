"""
Transformation
"""
from ... common.logger import log
from .transform import Transform
from .transformation import Transformation, IMAGE_COMPOSITION_OPERATOR, IMAGE_COMPOSITION_OPERAND
from .image_operations import ImageOperations
from PIL import Image, ImageOps
from itertools import product

TRANSFORMS2x2 = [Transform.IDENTITY, Transform.MIRROR, Transform.FLIP, Transform.ROTATE_90, Transform.ROTATE_180, Transform.ROTATE_270, Transform.CENTER_FLOOD_FILL, Transform.PIXELS_ADDED, Transform.PIXELS_REMOVED, Transform.PIXELS_ADDED_AND_REMOVED]

RMS_THRESHOLD = 94.0

class BinaryTransformation(Transformation):

    def __init__(self, tail, head, label):
        Transformation.__init__(self, tail, head, label)
        self.metadata = self.compute_metadata()
        self.transforms = self.compute_transformations()

    def compute_metadata(self):
        metadata = {}
        metadata['pixels_added'] = ImageOperations.calculate_minus(self.head.image, self.tail.image).load()
        metadata['pixels_removed'] = ImageOperations.calculate_minus(self.tail.image, self.head.image).load()
        return metadata

    def compute_transformations(self):
        transforms = []
        for transform in TRANSFORMS2x2:
            transformed_image = Transform.apply_transform(transform, self.tail.image, self.metadata)
            rms = ImageOperations.minus(self.head.image, transformed_image)
            if rms <= RMS_THRESHOLD:
                transforms.append((transform, rms, self.metadata))
        transforms.sort(key=lambda tup: tup[1])
        return transforms



