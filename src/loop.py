from src.rattle import Recover


class Loop(object):
    def __init__(self, head):

        self.head = head if head else -1
        self.body = []
        self.back_edges = []
        self.bbs = []
        self.key_value = None
        self._iterate_times = 0
        self._tx_sequence = None

    def __str__(self):
        return str(self.body)

    def __repr__(self):
        return str(self)

    @property
    def iterate_times(self):
        return self._iterate_times

    @iterate_times.setter
    def iterate_times(self, value):
        assert value >= 0
        self._iterate_times = value

    @property
    def tx_sequence(self):
        return self._tx_sequence

    @tx_sequence.setter
    def tx_sequence(self, value):
        self._tx_sequence = value

    def find_key_variable(self, ssa: Recover):
        # TODO: find key variable for the loop
        pass
