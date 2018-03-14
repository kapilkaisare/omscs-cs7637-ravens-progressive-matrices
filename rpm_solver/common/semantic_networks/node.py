"""
Node

"""
import uuid


class Node(object):

    def __init__(self, datum):
        self.id = uuid.uuid4()
        self.datum = datum

    def __repr__(self):
        return '<LinkLabel ' + self.id + ' >'

    def __str__(self):
        return self.__repr__()