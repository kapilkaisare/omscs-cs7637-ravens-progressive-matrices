from ..common.semantic_networks.node import Node

class ImageDatum(Node):

    def __init__(self, datum, identifier):
        Node.__init__(self, datum)
        self.id = identifier
