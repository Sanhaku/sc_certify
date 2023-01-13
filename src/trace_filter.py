from typing import List
from src.loop import Loop
from src.sym_exec.trace import Trace


def get_growth_traces(traces: List[Trace], loops: List[Loop]) -> List[Loop]:

    for loop in loops:
        idx = 0
        for key_insn in loop.key_variable:
            if key_insn.insn.name not in ['SLOAD']:
                continue
            selected_traces = []
            arg = key_insn.arguments[0]

            for trace in traces:
                growth_flag = False
                for analyzed_block in trace.analyzed_blocks:

                    for instruction in analyzed_block.block.insns:
                        if instruction.insn.name == 'SSTORE' and instruction.arguments[0] == arg:
                            if instruction.arguments[1].value == -1 and instruction.arguments[1].concrete_value == 0:
                                continue
                            growth_flag = True
                            break

                if growth_flag:
                    selected_traces.append(trace)

            loop.growth_traces[idx] = selected_traces
            idx += 1

    return loops
