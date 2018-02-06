from .difference import Difference

class Node(object):

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def has_same_attribute_keys_as(self, other_node):
        if (set(list(self.attributes.keys())) == set(list(other_node.attributes.keys()))):
            return True
        return False

    def minus(self, other_node):
        differences = {}
        for attribute, value in self.attributes.items():
            other_value = other_node.attributes[attribute]
            if other_value != value:
                differences[attribute] = Difference(value, other_value)
        return differences