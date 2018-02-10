class PatternTransformation(object):

    def __init__(self, first_pattern, second_pattern):
        self.from_pattern = first_pattern
        self.to_pattern = second_pattern
        self.correspondence = {}
        self.changes = {}

        self.establish_corresponding_nodes()
        self.observe_changes()

    def establish_corresponding_nodes(self):
        for node in self.from_pattern.nodes:
            similarity_scores = {}
            for other_node in self.to_pattern.nodes:
                similarity_scores[other_node] = node.find_similarity_with(other_node)
            self.correspondence[node] = max(similarity_scores, key=lambda key: similarity_scores[key])
    
    def observe_changes(self):
        for from_node, to_node in self.correspondence.items():
            self.changes[from_node] = to_node.minus(from_node)
    
    def log_correspondence(self):
        for k, v in self.correspondence.items():
            print k.name
            print v.name
            print "-"