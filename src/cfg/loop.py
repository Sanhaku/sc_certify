

class Loop(object):
    def __init__(self, head):

        self.head = head if head else -1
        self.body = []
        self.back_edges = []
        self.bbs = []

    def __str__(self):
        return str(self.body)

    def __repr__(self):
        return str(self)
