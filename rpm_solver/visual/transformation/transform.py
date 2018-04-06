from PIL import Image, ImageOps, ImageDraw

BLACK_PIXEL = (0, 0, 0, 255)

class Transform(object):
    IDENTITY = 'identity'
    MIRROR = 'mirror'
    FLIP = 'flip'
    ROTATE_90 = 'rotate90'
    ROTATE_180 = 'rotate180'
    ROTATE_270 = 'rotate270'
    UNION = 'union'
    INTERSECTION = 'intersection'
    XOR = 'xor'
    CENTER_FLOOD_FILL = 'center_flood_fill'
    PIXELS_ADDED = 'pixels_added'
    PIXELS_REMOVED = 'pixels_removed'

    @staticmethod
    def compute_identity_transform(image):
        transformed_image = image.copy()
        transformed_image.load()
        return transformed_image

    @staticmethod
    def compute_mirror_transform(image):
        transformed_image = ImageOps.mirror(image)
        transformed_image.load()
        return transformed_image

    @staticmethod
    def compute_flip_transform(image):
        transformed_image = ImageOps.flip(image)
        transformed_image.load()
        return transformed_image

    @staticmethod
    def compute_rotate_90_transform(image):
        transformed_image = image.rotate(90)
        transformed_image.load()
        return transformed_image

    @staticmethod
    def compute_rotate_180_transform(image):
        transformed_image = image.rotate(180)
        transformed_image.load()
        return transformed_image

    @staticmethod
    def compute_rotate_270_transform(image):
        transformed_image = image.rotate(270)
        transformed_image.load()
        return transformed_image

    @staticmethod
    def compute_center_flood_fill_transform(image):
        transformed_image = image.copy()
        width, height = transformed_image.size
        center = (int(0.5 * width), int(0.5 * height))
        ImageDraw.floodfill(transformed_image, xy=center, value=BLACK_PIXEL)
        return transformed_image

    @staticmethod
    def compute_union_transform(image_a, image_b):
        pass

    @staticmethod
    def compute_intersection_transform(image_a, image_b):
        pass

    @staticmethod
    def compute_xor_transform(image_a, image_b):
        pass

    @staticmethod
    def apply_transform(transform_name, image, data=None):
        if transform_name == Transform.IDENTITY:
            return Transform.compute_identity_transform(image)
        elif transform_name == Transform.MIRROR:
            return Transform.compute_mirror_transform(image)
        elif transform_name == Transform.FLIP:
            return Transform.compute_flip_transform(image)
        elif transform_name == Transform.ROTATE_90:
            return Transform.compute_rotate_90_transform(image)
        elif transform_name == Transform.ROTATE_180:
            return Transform.compute_rotate_180_transform(image)
        elif transform_name == Transform.ROTATE_270:
            return Transform.compute_rotate_270_transform(image)
        elif transform_name == Transform.CENTER_FLOOD_FILL:
            return Transform.compute_center_flood_fill_transform(image)
        elif transform_name == Transform.UNION:
            return Transform.compute_union_transform(image, data)
        elif transform_name == Transform.INTERSECTION:
            return Transform.compute_intersection_transform(image, data)
        elif transform_name == Transform.XOR:
            return Transform.compute_xor_transform(image, data)

