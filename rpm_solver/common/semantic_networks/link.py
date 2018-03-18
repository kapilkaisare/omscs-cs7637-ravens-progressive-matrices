"""
Link

"""
import uuid

class Link(object):

    def __init__(self, tail, head, label):
        self.id = uuid.uuid4()
        self.tail = tail
        self.head = head
        self.label = label

    def __repr__(self):
        return '<Link ' + str(self.id) + ' connecting ' + str(self.tail) + ' to ' + str(self.head) + ' labelled ' + str(self.label) + ' >'

    def __str__(self):
        return self.__repr__()