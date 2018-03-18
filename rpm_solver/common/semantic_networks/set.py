"""
Set
"""

import uuid

class Set(object):

    def __init__(self):
        self.id = uuid.uuid4()
        self.data = {}

    def __repr__(self):
        return '<Set ' + str(self.id) + ' >'

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.data)

    def add(self, item):
        self.data[item.id] = item