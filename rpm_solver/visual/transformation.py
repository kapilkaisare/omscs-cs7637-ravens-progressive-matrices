"""
Transformation
"""
from ..common.logger import log
from ..common.semantic_networks.link import Link
from PIL import Image, ImageOps
from itertools import product

class Transform(object):
    IDENTITY = 'identity'
    MIRROR = 'mirror'
    FLIP = 'flip'
    ROTATE_90 = 'rotate90'
    ROTATE_180 = 'rotate180'
    ROTATE_270 = 'rotate270'

class IMAGE_COMPOSITION_OPERATOR(object):
    NONE = "None"
    ADDITION = "addition"
    SUBTRACTION = "subtraction"

class IMAGE_COMPOSITION_OPERAND(object):
    NONE = "None"
    A_MINUS_B = "a_minus_b"
    B_MINUS_A = "b_minus_a"

TRANSFORMS = [Transform.IDENTITY, Transform.MIRROR, Transform.FLIP, Transform.ROTATE_90, Transform.ROTATE_180, Transform.ROTATE_270]

BLACK_PIXEL = (0, 0, 0, 255)

class Transformation(Link):

    def __init__(self, tail, head, label):
        Link.__init__(self, tail, head, label)
        self.id = self.label.value
        self.transform = self.compute_best_fit_similitude_transformation()

    def compute_best_fit_similitude_transformation(self):
        transforms = []
        for transform in TRANSFORMS:
            transformed_image = self.apply_transform(transform, self.tail.image)
            ic_operand, ic_operator, score = self.compute_image_composition_operand(transformed_image, self.head.image)
            transforms.append((transform, ic_operand, ic_operator, score))
        transforms.sort(key=lambda tup: tup[3])
        return transforms[-1]

    def apply_transform(self, transform_name, image):
        if transform_name == Transform.IDENTITY:
            return self.compute_identity_transform(image)
        elif transform_name == Transform.MIRROR:
            return self.compute_mirror_transform(image)
        elif transform_name == Transform.FLIP:
            return self.compute_flip_transform(image)
        elif transform_name == Transform.ROTATE_90:
            return self.compute_rotate_90_transform(image)
        elif transform_name == Transform.ROTATE_180:
            return self.compute_rotate_180_transform(image)

    def compute_image_composition_operand(self, image_a, image_b):
        a1b1 = self.compute_similarity(image_a, image_b, 1, 1)
        a1b0 = self.compute_similarity(image_a, image_b, 1, 0)
        a0b1 = self.compute_similarity(image_a, image_b, 0, 1)

        if a1b1 > a1b0 and a1b1 > a0b1:
            x = IMAGE_COMPOSITION_OPERAND.NONE
            operator = IMAGE_COMPOSITION_OPERATOR.NONE
            fitness_score = a1b1
        elif a1b0 > a1b1 and a1b0 > a0b1:
            x = IMAGE_COMPOSITION_OPERAND.B_MINUS_A
            operator = IMAGE_COMPOSITION_OPERATOR.ADDITION
            fitness_score = a1b0
        else:
            x = IMAGE_COMPOSITION_OPERAND.A_MINUS_B
            operator = IMAGE_COMPOSITION_OPERATOR.SUBTRACTION
            fitness_score = a0b1
        return (x, operator, fitness_score)

    def calculate_intersection(self, image_a, image_b):
        intersected_image = Image.new("RGBA", image_a.size, "white")
        intersected_image.load()
        pixels_a = image_a.pixels
        pixels_b = image_b.pixels
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == pixels_b[x, y] == BLACK_PIXEL:
                intersected_image.pixels[x, y] = BLACK_PIXEL
        return intersected_image

    def calculate_union(self, image_a, image_b):
        union_image = Image.new("RGBA", image_a.size, "white")
        union_image.load()
        pixels_a = image_a.pixels
        pixels_b = image_b.pixels
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == BLACK_PIXEL or pixels_b[x, y] == BLACK_PIXEL:
                union_image.pixels[x, y] = BLACK_PIXEL
        return union_image

    def calculate_minus(self, image_a, image_b):
        minus_image = Image.new("RGBA", image_a.size, "white")
        minus_image.load()
        pixels_a = image_a.pixels
        pixels_b = image_b.pixels
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == BLACK_PIXEL and pixels_b[x, y] != BLACK_PIXEL:
                minus_image.pixels[x, y] = BLACK_PIXEL
        return minus_image

    def compute_similarity(self, image_a, image_b, alpha, beta):
        a_intersection_b = self.calculate_intersection(image_a, image_b)
        a_minus_b = self.calculate_minus(image_a, image_b)
        b_minus_a = self.calculate_minus(image_a, image_b)
        f_a_intersection_b = self.calculate_feature(a_intersection_b)
        f_a_minus_b = self.calculate_feature(a_minus_b)
        f_b_minus_a = self.calculate_feature(b_minus_a)
        return f_a_intersection_b/(f_a_intersection_b + (alpha * f_a_minus_b) + (beta * f_b_minus_a))

    def calculate_feature(self, image):
        width, height = image.size
        return len([(x, y) for x, y in list(product(range(width), range(height))) if image.pixels[x, y] == BLACK_PIXEL])

    def compute_identity_transform(self, image):
        transformed_image = Image.new("RGBA", image.size, "white")
        transformed_image.load()
        transformed_image.pixels = image.pixels
        return transformed_image

    def compute_mirror_transform(self, image):
        transformed_image = ImageOps.mirror(image)
        transformed_image.load()
        return transformed_image

    def compute_flip_transform(self, image):
        transformed_image = ImageOps.flip(image)
        transformed_image.load()
        return transformed_image

    def compute_rotate_90_transform(self, image):
        transformed_image = image.rotate(90)
        transformed_image.load()
        return transformed_image

    def compute_rotate_180_transform(self, image):
        transformed_image = image.rotate(180)
        transformed_image.load()
        return transformed_image

    def compute_rotate_270_transform(self, image):
        transformed_image = image.rotate(270)
        transformed_image.load()
        return transformed_image

