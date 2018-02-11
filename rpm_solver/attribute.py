class Attribute(object):
    
    def __init__(self, node, value):
        self.type = "generic"
        self.node = node
        self.value = value
        self.parent = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ListAttribute(Attribute):
    def __init__(self, node, value):
        Attribute.__init__(self, node, value)
        self.type = "generic list"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return len(self.value) == len(other.value)
        return False


class Shape(Attribute):

    def __init__(self, node, value):
        Attribute.__init__(self, node, value)
        self.type = "shape"


class Fill(Attribute):

    def __init__(self, node, value):
        Attribute.__init__(self, node, value)
        self.type = "fill"


class Angle(Attribute):

    def __init__(self, node, value):
        Attribute.__init__(self, node, value)
        self.type = "angle"


class Size(Attribute):

    def __init__(self, node, value):
        Attribute.__init__(self, node, value)
        self.type = "angle"

class Inside(ListAttribute):

    def __init__(self, node, value):
        Attribute.__init__(self, node, value)
        self.type = "inside"