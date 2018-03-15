"""
Transformation
"""
from ..common.logger import log

class Attributes(object):
    SIZE = 'size'

class ChangeThresholds(object):
    SIZE = 1000

class SizeTransformations(object):
    EXPANDED = 'expanded'
    CONTRACTED = 'contracted'
    UNCHANGED ='unchanged'

class Transformation(object):

    def __init__(self, tail, head):
        self.tail = tail
        self.head = head
        self.transforms = {}
        self.compute_transforms()
        self.compute_union()

    def compute_transforms(self):
        self.compute_size_tranformation()

    def compute_size_tranformation(self):
        perceived_tail_size = self.tail.compute_perceived_size()
        perceived_head_size = self.head.compute_perceived_size()

        if perceived_tail_size - perceived_head_size > ChangeThresholds.SIZE:
            self.transforms[Attributes.SIZE] = SizeTransformations.CONTRACTED
        elif perceived_head_size - perceived_tail_size > ChangeThresholds.SIZE:
            self.transforms[Attributes.SIZE] = SizeTransformations.EXPANDED
        else:
            self.transforms[Attributes.SIZE] = SizeTransformations.UNCHANGED

    def compute_union(self):
        pass
