from collections import defaultdict
from src.cfg.loop import Loop
from src.sym_exec.trace import Trace
import src.rattle as rattle


class Analyze(object):
    def __init__(self, ssa: rattle.Recover, traces: list(Trace)):
        self.ssa = ssa
        self.traces = traces
        self.key_variables = None
        self.growth_traces = None
        pass

    def get_key_variables(self, ssa: rattle.Recover, loops: defaultdict(list(Loop))):
        # TODO: get_key_variables
        pass

    def get_growth_traces(self, traces: list(Trace), key_variables) -> list(Trace):
        # TODO: get_growth_traces
        pass

    def generate_sequence(self, growth_traces: list(Trace), key_variables, iterate_times: defaultdict):
        # TODO: generate_sequence
        pass
