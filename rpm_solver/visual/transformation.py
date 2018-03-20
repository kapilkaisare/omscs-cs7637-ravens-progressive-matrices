"""
Transformation
"""
from ..common.logger import log
from ..common.semantic_networks.link import Link
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

TRANSFORMS2x2 = [Transform.IDENTITY, Transform.MIRROR, Transform.FLIP, Transform.ROTATE_90, Transform.ROTATE_180, Transform.ROTATE_270]

TRANSFORMS3x3 = [Transform.UNION, Transform.INTERSECTION, Transform.XOR]

BLACK_PIXEL = (0, 0, 0, 255)

class Transformation(Link):

    def __init__(self, tail, head, label):
        Link.__init__(self, tail, head, label)
        self.id = self.label.value
        self.union = None
        self.intersection = None
        self.xor = None
        
        if type(tail) is tuple:
            self.union = self.calculate_union(tail[0], tail[1])
            self.intersection = self.calculate_intersection(tail[0], tail[1])
            self.xor = self.calculate_xor(tail[0], tail[1])

        self.transform = self.compute_best_fit_similitude_transformation()

    def compute_best_fit_similitude_transformation(self):
        transforms = []
        if self.union == None:
            for transform in TRANSFORMS2x2:
                transformed_image = Transform.apply_transform(transform, self.tail.image)
                ic_operand, ic_operator, score = self.compute_image_composition_operand(transformed_image, self.head.image)
                transforms.append((transform, ic_operand, ic_operator, score))
            transforms.sort(key=lambda tup: tup[3])
            return transforms[-1]
        else:
            for transform in TRANSFORMS3x3:
                transformed_image = Transform.apply_transform(transform, self.tail.image)
                ic_operand, ic_operator, score = self.compute_image_composition_operand(transformed_image, self.head.image)
                transforms.append((transform, ic_operand, ic_operator, score))
            transforms.sort(key=lambda tup: tup[3])
            return transforms[-1]


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
        intersected_image_pixels = intersected_image.load()
        pixels_a = image_a.load()
        pixels_b = image_b.load()
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == pixels_b[x, y] == BLACK_PIXEL:
                intersected_image_pixels[x, y] = BLACK_PIXEL
        return intersected_image

    def calculate_union(self, image_a, image_b):
        union_image = Image.new("RGBA", image_a.size, "white")
        union_image_pixels = union_image.load()
        pixels_a = image_a.load()
        pixels_b = image_b.load()
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == BLACK_PIXEL or pixels_b[x, y] == BLACK_PIXEL:
                union_image_pixels[x, y] = BLACK_PIXEL
        return union_image

    def calculate_xor(self, image_a, image_b):
        xor_image = Image.new("RGBA", image_a.size, "white")
        xor_image_pixels = xor_image.load()
        pixels_a = image_a.load()
        pixels_b = image_b.load()
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if (pixels_a[x, y] == BLACK_PIXEL and pixels_b[x, y] != BLACK_PIXEL) or (pixels_a[x, y] != BLACK_PIXEL and pixels_b[x, y] == BLACK_PIXEL):
                xor_image_pixels[x, y] = BLACK_PIXEL
        return xor_image

    def calculate_minus(self, image_a, image_b):
        minus_image = Image.new("RGBA", image_a.size, "white")
        minus_image_pixels = minus_image.load()
        pixels_a = image_a.load()
        pixels_b = image_b.load()
        width, height = image_a.size
        for x, y in list(product(range(width), range(height))):
            if pixels_a[x, y] == BLACK_PIXEL and pixels_b[x, y] != BLACK_PIXEL:
                minus_image_pixels[x, y] = BLACK_PIXEL
        return minus_image

    def compute_similarity(self, image_a, image_b, alpha, beta):
        a_intersection_b = self.calculate_intersection(image_a, image_b)
        a_minus_b = self.calculate_minus(image_a, image_b)
        b_minus_a = self.calculate_minus(image_a, image_b)
        f_a_intersection_b = float(self.calculate_feature(a_intersection_b))
        f_a_minus_b = float(self.calculate_feature(a_minus_b))
        f_b_minus_a = float(self.calculate_feature(b_minus_a))
        return f_a_intersection_b/(f_a_intersection_b + (float(alpha) * f_a_minus_b) + (float(beta) * f_b_minus_a))

    def calculate_feature(self, image):
        width, height = image.size
        image_pixels = image.load()
        return len([(x, y) for x, y in list(product(range(width), range(height))) if image_pixels[x, y] == BLACK_PIXEL])


