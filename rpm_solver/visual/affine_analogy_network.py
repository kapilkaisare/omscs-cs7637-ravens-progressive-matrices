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
        if len(self.nodes) == 3:
            transform_ab = links["AB"].transform
            transform_ac = links["AC"].transform
            if transform_ab[3] > transform_ac[3]:
                return ('horizontal', transform_ab)
            else:
                return ('vertical', transform_ac)
        else:
            return (sorted([\
                ('bc', links["BC"].transform),\
                ('dg', links["DG"].transform),\
                ('ac', links["AC"].transform),\
                ('ag', links["AG"].transform),\
                ('ef', links["EF"].transform),\
                ('eh', links["EH"].transform),\
                ('df', links["DF"].transform),\
                ('bh', links["BH"].transform),\
                ('gh', links["GH"].transform),\
                ('cf', links["CF"].transform)\
            ], key=lambda x: x[1][3]))[-1]

    def establish_horizontal_transformations(self):
        if len(self.nodes) == 3:
            self.establish_2x2transformation('A', 'B')
        else:
            self.establish_3x3transformation('A', 'B', 'C')
            self.establish_3x3transformation('D', 'E', 'F')

    def establish_vertical_transformations(self):
        if len(self.nodes) == 3:
            self.establish_2x2transformation('A', 'C')
        else:
            self.establish_3x3transformation('A', 'D', 'G')
            self.establish_3x3transformation('B', 'E', 'H')

    def establish_2x2transformation(self, tail_key, head_key):
        log("[AffineAnalogyNetwork/establish_2x2transformation] " + tail_key + ", " + head_key)
        tail_node = self.nodes.data[tail_key]
        head_node = self.nodes.data[head_key]
        transform_key = tail_key + head_key
        self.construct_link(transform_key, tail_node, head_node)

    def establish_3x3transformation(self, tail_1_key, tail_2_key, head_key):
        log("[AffineAnalogyNetwork/establish_3x3transformation] " + tail_1_key + ", " + tail_2_key + " ," + head_key)
        tail1_node = self.nodes.data[tail_1_key]
        tail2_node = self.nodes.data[tail_2_key]
        head_node = self.nodes.data[head_key]
        transform_key = tail_1_key + tail_2_key + head_key
        self.construct_link(transform_key, (tail1_node, tail2_node), head_node)

