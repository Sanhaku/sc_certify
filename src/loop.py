import logging
from src.rattle import Recover
from src.utils import get_source

logger = logging.getLogger(__name__)


class Loop(object):
    def __init__(self, head):

        self.head = head if head else -1
        self.body = []
        self.back_edges = []
        self.bbs = []
        self._key_variable = None
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

    @property
    def key_variable(self):
        return self._key_variable

    @key_variable.setter
    def key_variable(self, value):
        self._key_variable = value

    def find_key_variable(self, ssa: Recover):

        for f in ssa.functions:
            for b in f.blocks:
                if b.offset == self.head:
                    head_block = b
                    break

        if len(head_block.insns) < 2 or head_block.insns[-2].insn.name != 'ISZERO':
            return
        judge_arg = head_block.insns[-2].arguments[0]

        writer_insn = judge_arg.writer
        source = []
        get_source(writer_insn, source, [])

        if len(source) == 0:
            logger.warning("Cannot find key variable")
            return

        self._key_variable = source
        # self._key_variable = []
        # for s in source:
        #     if s.insn.name == 'CALLDATALOAD':
        #         self._key_variable.append(('CALLDATALOAD', s.arguments[0]))
        #     elif s.insn.name == 'SLOAD':
        #         self._key_variable.append(('SLOAD', s.arguments[0]))
