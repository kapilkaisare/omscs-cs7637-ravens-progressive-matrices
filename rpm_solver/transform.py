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
        self.transformation_details = self.translated_target - self.source

    def __eq__(self, other):
        source_analogy = PatternAnalogy(other.source, self.source).analogues
        other_translated_difference = other.transformation_details.translate(source_analogy)
        # PatternDifference
        return self.transformation_details == other_translated_difference


    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "<PatternTransform: From " + self.source.__str__() + " to " + self.translated_target.__str__() + " >"

    def find_corresponding_nodes(self):
        for node_name, node in self.source.nodes.items():
            similarity_scores = {}
            for other_node_name, other_node in self.target.nodes.items():
                similarity_score = NodeSimilarity(node, other_node).similarity
                similarity_scores[other_node] = similarity_score
            corresponding_node_name = max(similarity_scores,
                key=lambda key: similarity_scores[key]).name
            self.corresponding_nodes[corresponding_node_name] = node_name

