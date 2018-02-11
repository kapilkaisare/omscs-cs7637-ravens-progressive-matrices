from .similarity import NodeSimilarity

class PatternTransformation(object):

    def __init__(self, first_pattern, second_pattern):
        self.from_pattern = first_pattern
        self.to_pattern = second_pattern

        self.correspondence = {}
        self.nodes_changed = {}
        self.nodes_added = {} #tbd
        self.nodes_deleted = {} #tbd

        self.establish_corresponding_nodes()
        self.observe_changes()


    def establish_corresponding_nodes(self):
        for node_name, node in self.from_pattern.nodes.items():
            similarity_scores = {}
            for other_node_name, other_node in self.to_pattern.nodes.items():
                similarity_score = NodeSimilarity(node, other_node).similarity
                similarity_scores[other_node] = similarity_score
            self.correspondence[node] = max(similarity_scores, key=lambda key: similarity_scores[key])


    def observe_changes(self):
        for from_node, to_node in self.correspondence.items():
            self.nodes_changed[from_node] = to_node.minus(from_node)


    def changes_observed(self):
        changed = False
        for node, changes in self.nodes_changed.items():
            if any(changes):
                changed = True
        return changed


    def log_correspondence(self):
        for k, v in self.correspondence.items():
            print k.name
            print v.name
            print "-"


    def log_changes(self):
        for k, v in self.nodes_changed.items():
            print k.name
            for m, n in v.items():
                print m + ": " + n.log()
