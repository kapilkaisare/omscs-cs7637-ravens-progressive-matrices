class Analogy(object):
    
    def __init__(self, pattern1, pattern2):
        self.analogues = {}
        self.reference_pattern = pattern1
        self.compared_pattern = pattern2
        self.detect_analogues()

    def detect_analogues(self):
        for node in self.reference_pattern.nodes:
            analogy_scores = {}
            for other_node in self.compared_pattern.nodes:
                analogy_scores[other_node] = node.find_analogy_with(other_node)
            self.analogues[node] = max(analogy_scores, key=lambda key: analogy_scores[key])

    def get_analogue_for(self, node):
        for test_node, analogue in self.analogues.items():
            if analogue == node:
                return test_node
        return None

    def log_analogues(self):
        for k, v in self.analogues.items():
            print k.name
            print v.name
            print "-"