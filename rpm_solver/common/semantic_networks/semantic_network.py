"""
Semantic Network
"""
import uuid

from .set import Set
from .node import Node
from .link_label import LinkLabel
from .link import Link

class SemanticNetwork(object):

    def __init__(self):
        self.id = uuid.uuid4()
        self.nodes = Set()
        self.links = Set()

    def construct_node(self, node_data):
        node = Node(node_data)
        self.nodes.add(node)
        return node.id

    def construct_link(self, label_data, tail, head):
        link_label = LinkLabel(label_data)
        link = Link(tail, head, link_label)
        self.links.add(link)
        return link.id

    def get_tails(self, node):
        return {k: v for k, v in self.links.data.iteritems() if v.tail.id == node.id }

    def get_heads(self, node):
        return {k: v for k, v in self.links.data.iteritems() if v.head.id == node.id }

    def get_tail(self, link):
        return link.tail

    def get_head(self, link):
        return link.head

    def get_link_label(self, link):
        return link.label