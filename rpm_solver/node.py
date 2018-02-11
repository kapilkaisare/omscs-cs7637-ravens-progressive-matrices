from .attribute import Attribute, Shape, Fill, Angle, Size, Inside
from .difference import Difference

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
        self.attributes = {}
        self.parent = None
        self.load_attributes(attributes)

    def __eq__(self, other):
        if not len(self.attributes.keys()) == len(other.attributes.keys()):
            return False

        for attribute_key, attribute in self.attributes.items():
            if attribute != other.attributes[attribute_key]:
                return False

        return True


    def __ne__(self, other):
        return not self.__eq__(other)


    def load_attributes(self, attributes):
        for attribute_type, attribute_value in attributes.items():
            new_attribute = None
            if attribute_type == "shape":
                new_attribute = Shape(attribute_value)
            elif attribute_type == "fill":
                new_attribute = Fill(attribute_value)
            elif attribute_type == "angle":
                new_attribute = Angle(attribute_value)
            elif attribute_type == "size":
                new_attribute = Size(attribute_value)
            elif attribute_type == "inside":
                attribute_value_list = attribute_value.split(",")
                new_attribute = Inside(attribute_value_list)
            else:
                new_attribute = Attribute(attribute_value)
            new_attribute.parent = self
            self.attributes[attribute_type] = new_attribute

    def translate(self, translation_key):
        print "Translation key:"
        print translation_key
        translated_node = Node(translation_key[self.name], {})
        for attribute_key, attribute in self.attributes.items():
            translated_attribute = attribute.translate(translation_key)
            translated_attribute.parent = translated_node
        return translated_node

    def is_like(self, other):
        if not len(self.attributes.keys()) == len(other.attributes.keys()):
            return False

        for attribute_key, attribute in self.attributes.items():
            if attribute_key != "shape" and attribute != other.attributes[attribute_key]:
                return False

        return True


    def minus(self, other_node):
        differences = {}
        for attribute_key, value in self.attributes.items():
            if attribute_key in other_node.attributes:
                other_value = other_node.attributes[attribute_key]
                if other_value != value:
                    differences[attribute_key] = Difference(value, other_value)
        return differences

    def find_analogy_with(self, other_node):
        analogy_score = 0
        for attribute_name, addendum in ANALOGY_GRADES.items():
            if attribute_name in self.attributes and attribute_name in other_node.attributes and self.attributes[attribute_name] == other_node.attributes[attribute_name]:
                analogy_score = analogy_score + addendum;
        return analogy_score

    def apply_changes(self, changes):
        new_attribute_set = dict(self.attributes)
        for changed_key, difference in changes.items():
            if changed_key in new_attribute_set:
                new_attribute_set[changed_key] = difference.apply_to(new_attribute_set[changed_key])
        return new_attribute_set

    def log_attributes(self):
        for attribute_key, attribute in self.attributes.items():
            print "attribute_key: " + attribute_key
            print attribute
            print attribute.value