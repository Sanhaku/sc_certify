from z3 import z3

from src.cfg.util.z3_extra_util import concrete

class Stack(list):
    def __init__(self, *args):
        super(Stack, self).__init__(*args)

    def push(self, v):
        self.append(v)

    def append(self, v):
        if concrete(v):
            v %= 2 ** 256
        super(Stack, self).append(v)

class Memory():
    def __init__(self, *args):
        self.memory = bytearray(*args)
        self._check_initialized = False
        self.initialized = set()

    def __getitem__(self, index):
        if isinstance(index, slice):
            initialized = all(i in self.initialized for i in range(index.start or 0, index.stop, index.step or 1))
        else:
            initialized = index in self.initialized
        if not self._check_initialized or initialized:
            return self.memory[index]
        # else:
        #     raise UninitializedRead(index)

    def __setitem__(self, index, v):
        if isinstance(index, slice):
            for i in range(index.start or 0, index.stop, index.step or 1):
                self.initialized.add(i)
        else:
            self.initialized.add(index)
        self.memory[index] = v

    def set_enforcing(self, enforcing=True):
        self._check_initialized = enforcing

    def extend(self, start, size):
        if len(self.memory) < start + size:
            self.memory += bytearray(start + size - len(self.memory))

    def __len__(self):
        return len(self.memory)

