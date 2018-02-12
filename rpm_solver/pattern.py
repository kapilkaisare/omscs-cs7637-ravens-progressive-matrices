from .difference import PatternDifference

class Pattern(object):

    def __init__(self):
        self.nodes = {}

    def __eq__(self, other):
        for node in self.nodes.values():
            matching_nodes = [matching_node for matching_node in other.nodes.values() if node == matching_node]
            if not any(matching_nodes):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __sub__(self, other):
        changes = {}

        for node_name, node in other.nodes.items():
            if node_name in self.nodes:
                changes[node_name] = self.nodes[node_name] - node

        return PatternDifference(changes)

    def __str__(self):
        node_str = ""
        for node_name, node in self.nodes.items():
            node_str = node_str + " " + node.__str__()
        return "<Pattern Nodes - " + node_str + " >"


    def add_node(self, node):
        node.parent = self
        self.nodes[node.name] = node

    def translate(self, node_table):
        translated_target = Pattern()
        for node_name, node in self.nodes.items():
            translated_node = node.translate(node_table)
            translated_target.add_node(translated_node)
        return translated_target
