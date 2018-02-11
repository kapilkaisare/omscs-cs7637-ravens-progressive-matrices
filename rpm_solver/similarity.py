SIMILARITY_GRADES = {
    "shape": 10,
    "size": 1,
    "fill": 1,
    "inside": 1,
    "overlaps": 1
}

class NodeSimilarity(object):
    
    def __init__(self, one_node, other_node):
        self.first = one_node
        self.second = other_node
        self.similarity = self.calculate_similarity()

    def calculate_similarity(self):
        similarity_score = 0
        for attribute_name, addendum in SIMILARITY_GRADES.items():
            if not self.both_nodes_have_attribute(attribute_name):
                break
            first_value = self.first.attributes[attribute_name]
            second_value = self.second.attributes[attribute_name]
            if first_value == second_value:
                similarity_score = similarity_score + addendum;
        return similarity_score

    def both_nodes_have_attribute(self, attribute_name):
        return (attribute_name in self.first.attributes) and (
            attribute_name in self.second.attributes)
