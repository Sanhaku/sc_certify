from typing import List
from src.loop import Loop
from src.sym_exec.trace import Trace
from src.tx_seq import TxSeq


class SeqGenerator(object):
    def __init__(self, loops: List[Loop]):
        self.loops = loops

    def execute(self, timeout=300_000) -> TxSeq:
        # TODO: find a transaction sequence that will make the loop iterate iterate_times
        for loop in self.loops:
            loop.tx_sequence = TxSeq()
