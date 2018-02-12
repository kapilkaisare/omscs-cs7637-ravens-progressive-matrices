from .difference import Difference

class Attribute(object):
    
    def __init__(self, value):
        self.type = "generic"
        self.value = value
        self.parent = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return False

    def __sub__(self, other):
        if self.value != other.value:
            return Difference(self.type, other.value, self.value)
        return None

    def __str__(self):
        return "<Attribute (" + self.type + "): " + self.value +  ">"

    def __ne__(self, other):
        return not self.__eq__(other)

    def translate(self, translation_key):
        return type(self)(self.value)


class ListAttribute(Attribute):
    def __init__(self, value):
        Attribute.__init__(self, value)
        self.type = "generic list"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return len(self.value) == len(other.value)
        return False

    def translate(self, translation_key):
        new_value = [translation_key[v] for v in self.value if v in translation_key]
        return type(self)(new_value)



class Shape(Attribute):

    def __init__(self, value):
        Attribute.__init__(self, value)
        self.type = "shape"


class Fill(Attribute):

    def __init__(self, value):
        Attribute.__init__(self, value)
        self.type = "fill"


class Angle(Attribute):

    def __init__(self, value):
        Attribute.__init__(self, value)
        self.type = "angle"



class Size(Attribute):

    def __init__(self, value):
        Attribute.__init__(self, value)
        self.type = "size"

class Inside(ListAttribute):

    def __init__(self, value):
        Attribute.__init__(self, value)
        self.type = "inside"