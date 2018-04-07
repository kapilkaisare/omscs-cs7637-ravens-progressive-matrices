from ..common.semantic_networks.semantic_network import SemanticNetwork
from ..common.semantic_networks.link_label import LinkLabel
from ..common.logger import log
from .image_datum import ImageDatum
from .transformation.binary_tranformation import BinaryTransformation

class ImageAnalogyNetwork2x2(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)

    def construct_node(self, image_node_data, image_label):
        node = ImageDatum(image_node_data, image_label)
        self.nodes.add(node)
        return node.id

    def construct_link(self, label_data, tail, head):
        link_label = LinkLabel(label_data)
        link = BinaryTransformation(tail, head, link_label)
        self.links.add(link)
        return link.id

    def establish_transformations(self):
        self.establish_horizontal_transformations()
        self.establish_vertical_transformations()

    def get_transforms(self):
        links = self.links.data
        transforms = []
        for transform in links["AB"].transforms:
            transforms.append(('horizontal', transform[0], transform[1], transform[2]))
        for transform in links["AC"].transforms:
            transforms.append(('vertical', transform[0], transform[1], transform[2]))
        transforms.sort(key=lambda tup: tup[2])
        return transforms

    def establish_horizontal_transformations(self):
        self.establish_transformation('A', 'B')

    def establish_vertical_transformations(self):
        self.establish_transformation('A', 'C')

    def establish_transformation(self, tail_key, head_key):
        tail_node = self.nodes.data[tail_key]
        head_node = self.nodes.data[head_key]
        transform_key = tail_key + head_key
        self.construct_link(transform_key, tail_node, head_node)


