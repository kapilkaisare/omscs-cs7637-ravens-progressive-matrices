"""
    Attribute definitions.
"""
from exceptions import UnknownShapeException, UnknownSizeException, UnknownFillException, BadAngleException, NotAListException, AttributeMismatchException

class Attribute(object):

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        classes_match = self.__class__ == other.__class__
        if classes_match:
            return self.value == other.value
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ListAttribute(Attribute):
    def __init__(self, value):
        if type(value) != list:
            raise NotAListException()
        Attribute.__init__(value)


class Shape(Attribute):

    valid_shapes = ['square', 'diamond', 'triangle', 'right triangle', 'star', 'circle', 'rectangle', 'octagon', 'heart', 'pacman']

    def __init__(self, value):
        if value not in self.valid_shapes:
            raise UnknownShapeException()
        Attribute.__init__(value)

class Size(Attribute):
    
    valid_sizes = ['very small', 'small', 'medium', 'large', 'very large', 'huge']

    def __init__(self, value):
        if value not in self.valid_sizes:
            raise UnknownSizeException()
        Attribute.__init__(value)

class Fill(Attribute):

    valid_fills = ['yes', 'no']

    def __init__(self, value):
        if value not in self.valid_fills:
            raise UnknownFillException()
        Attribute.__init__(value)

class Angle(Attribute):
    def __init__(self, value):
        if not (0 < value < 360):
            raise BadAngleException()
        Attribute.__init__(value)

class Above(ListAttribute):
    pass

class LeftOf(ListAttribute):
    pass

class AttributeChange(object):

    def __init__(self, before, after):
        if before.__class__ != after.__class__:
            raise AttributeMismatchException()
        self.before = before
        self.after = after

    def apply(self, target):
        if target.__class__ != self.before.__class__:
            raise AttributeMismatchException()
        elif self.before.value == target.before.value:
            return target.__class__(self.after.value)


# class AngleChange(AttributeChange):

#     def apply(self, target):
#         if target.__class__ != self.before.__class__:
#             raise AttributeMismatchException()