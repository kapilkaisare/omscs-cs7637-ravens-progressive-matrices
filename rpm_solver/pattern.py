from .transformation import Transformation

class Pattern(object):

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def transforms_to(self, other_pattern):
        return Transformation(self, other_pattern)