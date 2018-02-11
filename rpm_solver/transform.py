from .similarity import NodeSimilarity
from .analogy import PatternAnalogy
from .pattern import Pattern

class PatternTransform(object):

    def __init__(self, first, second):
        self.source = first
        self.target = second

        self.corresponding_nodes = {}
        self.find_corresponding_nodes()

        self.translated_target = self.target.translate(self.corresponding_nodes)

    def __eq__(self, other):
        source_analogy = PatternAnalogy(self.source, other.source).analogues
        print source_analogy
        morphed_target = self.translated_target.translate(source_analogy)
        return morphed_target == other.translated_target

    def __ne__(self, other):
        return not self.__eq__(other)

    def find_corresponding_nodes(self):
        for node_name, node in self.source.nodes.items():
            similarity_scores = {}
            for other_node_name, other_node in self.target.nodes.items():
                similarity_score = NodeSimilarity(node, other_node).similarity
                similarity_scores[other_node] = similarity_score
            corresponding_node_name = max(similarity_scores,
                key=lambda key: similarity_scores[key]).name
            self.corresponding_nodes[corresponding_node_name] = node_name

