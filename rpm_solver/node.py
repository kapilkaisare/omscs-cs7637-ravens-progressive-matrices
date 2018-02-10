from .difference import Difference

SIMILARITY_GRADES = {
    "shape": 10,
    "size": 1,
    "fill": 1,
    "inside": 1,
    "overlaps": 1
}

ANALOGY_GRADES = {
    "shape": 1,
    "size": 10,
    "fill": 10,
    "inside": 10,
    "overlaps": 10
}

class Node(object):

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def has_same_attribute_keys_as(self, other_node):
        if (set(list(self.attributes.keys())) == set(list(other_node.attributes.keys()))):
            return True
        return False

    def has_similar_attribute_keys_as(self, other_node):
        pass

    def minus(self, other_node):
        differences = {}
        for attribute, value in self.attributes.items():
            if attribute in other_node.attributes:
                other_value = other_node.attributes[attribute]
                if other_value != value:
                    differences[attribute] = Difference(value, other_value)
        return differences

    def find_similarity_with(self, other_node):
        similarity_score = 0
        for attribute, addendum in SIMILARITY_GRADES.items():
            if attribute in self.attributes and attribute in other_node.attributes and self.attributes[attribute] == other_node.attributes[attribute]:
                similarity_score = similarity_score + addendum;
        return similarity_score

    def find_analogy_with(self, other_node):
        analogy_score = 0
        for attribute, addendum in ANALOGY_GRADES.items():
            if attribute in self.attributes and attribute in other_node.attributes and self.attributes[attribute] == other_node.attributes[attribute]:
                analogy_score = analogy_score + addendum;
        return analogy_score
    
    def log(self):
        print self.name
        print self.attributes