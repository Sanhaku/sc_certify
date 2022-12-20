class Analyze(object):
    def __init__(self, ssa, traces):
        self.ssa = ssa
        self.traces = traces
        self.key_variables = None
        self.growth_traces = None
        pass

    def get_key_variables(self, ssa, loops):
        # TODO: get_key_variables
        pass

    def get_growth_traces(self, traces, key_variables):
        # TODO: get_growth_traces
        pass

    def generate_sequence(self, growth_traces, key_variables, iterate_times):
        # TODO: generate_sequence
        pass
