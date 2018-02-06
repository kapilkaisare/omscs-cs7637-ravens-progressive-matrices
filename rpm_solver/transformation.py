class Transformation(object):

    def __init__(self, first_pattern, second_pattern):
        self.from_pattern = first_pattern
        self.to_pattern = second_pattern
        self.analogues = {}
        self.node_differences = {}

    def find_analogue(self, reference_node, pattern):
        for compared_node in pattern.nodes:
            if reference_node.has_same_attribute_keys_as(compared_node):
                return compared_node

    def diff(self):
        for node in self.from_pattern.nodes:
            analogue = self.find_analogue(node, self.to_pattern)
            if analogue is not None:
                self.analogues[node] = analogue
        for reference_node, compared_node in self.analogues.items():
            self.node_differences[(reference_node, compared_node)] = compared_node.minus(reference_node)
        return self.node_differences