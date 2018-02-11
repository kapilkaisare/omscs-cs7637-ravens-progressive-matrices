from .pattern_transformation import PatternTransformation

class Pattern(object):

    def __init__(self):
        self.nodes = {}

    def __eq__(self, other):
        for node in self.nodes.values():
            matching_nodes = [matching_node for matching_node in other.nodes.values() if node == matching_node]
            if not any(matching_nodes):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_node(self, node):
        node.parent = self
        self.nodes[node.name] = node

    def transforms_to(self, other_pattern):
        return PatternTransformation(self, other_pattern)

    def log_nodes(self):
        for node in self.nodes:
            node.log()