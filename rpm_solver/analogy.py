class Analogy(object):
    
    def __init__(self, pattern1, pattern2):
        self.analogues = {}
        self.reference_pattern = pattern1
        self.compared_pattern = pattern2
        self.detect_analogues()

    def detect_analogues(self):
        for node_name, node in self.reference_pattern.nodes.items():
            analogy_scores = {}
            for other_node_name, other_node in self.compared_pattern.nodes.items():
                analogy_scores[other_node] = node.find_analogy_with(other_node)
            self.analogues[node] = max(analogy_scores, key=lambda key: analogy_scores[key])

    def get_analogue_for(self, node):
        for test_node, analogue in self.analogues.items():
            if analogue == node:
                return test_node
        return None


class PatternAnalogy(object):

    def __init__(self, one_pattern, other_pattern):
        self.reference_pattern = one_pattern
        self.compared_pattern = other_pattern

        self.analogues = {}

        self.make_analogies()

    def make_analogies(self):
        reference_items = self.reference_pattern.nodes.items()
        compared_items = self.compared_pattern.nodes.items()
        for node_name, node in reference_items:
            analogy_scores = {}
            for other_node_name, other_node in compared_items:
                analogy_scores[other_node] = node.find_analogy_with(other_node)
            analogue = max(analogy_scores,
                key=lambda key: analogy_scores[key]).name
            self.analogues[node_name] = analogue