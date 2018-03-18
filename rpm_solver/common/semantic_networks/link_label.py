"""
Link label
"""
import uuid

class LinkLabel(object):

    def __init__(self, value):
        self.id = uuid.uuid4()
        self.value = value

    def __repr__(self):
        return '<LinkLabel ' + str(self.id) + ' ' + str(self.value) + ' >'

    def __str__(self):
        return self.__repr__()
