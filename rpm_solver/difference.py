class Difference(object):

    def __init__(self, attribute_type, from_value, to_value):
        self.attribute_type = attribute_type
        self.from_value = from_value
        self.to_value = to_value

    def __str__(self):
        from_value = self.from_value
        to_value =self.to_value
        if type(from_value) == list:
            from_value = "<list>"
        if type(to_value) == list:
            to_value = "<list>"
        return "<Difference: " + self.attribute_type + " - from " + from_value + " to " + to_value + " >"
    
    def apply_to(self, original_value):
        if self.from_value == original_value:
            return self.to_value
        return original_value


class PatternDifference(object):

    def __init__(self, node_changes):
        self.node_changes = node_changes

    def __eq__(self, other):
        for node_key, node_attributes in self.node_changes.items():
            other_changes = other.node_changes[node_key]
            for attribute_key, attribute in node_attributes.items():
                if attribute_key not in other_changes:
                    return False
                print "Ole"
                print attribute_key
                print attribute
                print other_changes[attribute_key]
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        node_changes_str = ""
        for node_name, attribute_changes in self.node_changes.items():
            attribute_changes_str = ""
            for attribute_key, attr in attribute_changes.items():
                attribute_changes_str = attribute_changes_str + attr.__str__()
            node_changes_str = node_changes_str + " < Node : " + node_name + " - " + attribute_changes_str + " >"
        return "<PatternDifference: " + node_changes_str + " >"

    def translate(self, translation_key):
        translated_changes = {}
        for node_name, attribute_changes in self.node_changes.items():
            translated_key = translation_key[node_name]
            translated_changes[translated_key] = attribute_changes
        
        return PatternDifference(translated_changes)