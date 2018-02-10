from .pattern_transformation import PatternTransformation

class Pattern(object):

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def transforms_to(self, other_pattern):
        return PatternTransformation(self, other_pattern)

    def log_nodes(self):
        for node in self.nodes:
            node.log()