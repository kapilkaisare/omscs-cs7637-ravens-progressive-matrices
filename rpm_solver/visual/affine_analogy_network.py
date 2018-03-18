"""
Affine Analogy Network
"""
from ..common.semantic_networks.semantic_network import SemanticNetwork
from ..common.semantic_networks.link_label import LinkLabel
from ..common.logger import log
from .image_datum import ImageDatum
from .transformation import Transformation

class AffineAnalogyNetwork(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)

    def construct_node(self, image_node_data, image_label):
        node = ImageDatum(image_node_data, image_label)
        self.nodes.add(node)
        return node.id

    def construct_link(self, label_data, tail, head):
        link_label = LinkLabel(label_data)
        link = Transformation(tail, head, link_label)
        self.links.add(link)
        return link.id

    def establish_transformations(self):
        self.establish_horizontal_transformations()
        self.establish_vertical_transformations()

    def get_best_similitude_transform(self):
        log("[AffineAnalogyNetwork/get_best_similitude_transform]")
        links = self.links.data
        if len(self.nodes) == 4:
            transform_ab = links["AB"].transform
            transform_ac = links["AC"].transform
            if transform_ab[3] > transform_ac[3]:
                return ('horizontal', transform_ab)
            else:
                return ('vertical', transform_ac)
        else:
            pass

    def establish_horizontal_transformations(self):
        if len(self.nodes) == 4:
            self.establish_transformation('A', 'B')
            self.establish_transformation('C', 'D')
        else:
            self.establish_transformation('A', 'B')
            self.establish_transformation('B', 'C')
            self.establish_transformation('D', 'E')
            self.establish_transformation('E', 'F')
            self.establish_transformation('G', 'H')
            self.establish_transformation('H', 'I')

    def establish_vertical_transformations(self):
        if len(self.nodes) == 4:
            self.establish_transformation('A', 'C')
            self.establish_transformation('B', 'D')
        else:
            self.establish_transformation('A', 'D')
            self.establish_transformation('D', 'G')
            self.establish_transformation('B', 'E')
            self.establish_transformation('E', 'H')
            self.establish_transformation('C', 'F')
            self.establish_transformation('F', 'I')

    def establish_transformation(self, tail_key, head_key):
        log("[AffineAnalogyNetwork/establish_transformation] " + tail_key + ", " + head_key)
        tail_node = self.nodes.data[tail_key]
        head_node = self.nodes.data[head_key]
        transform_key = tail_key + head_key
        self.construct_link(transform_key, tail_node, head_node)
