class Difference(object):

    def __init__(self, from_value, to_value):
        self.from_value = from_value
        self.to_value = to_value
    
    def apply_to(self, original_value):
        if self.from_value == original_value:
            return self.to_value
        return original_value