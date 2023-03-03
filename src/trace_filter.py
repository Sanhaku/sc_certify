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
                            # rule out situations like set zero and newArray[]
                            if instruction.arguments[1].value == -1 and instruction.arguments[1].concrete_value == 0:
                                continue
                            writer = instruction.arguments[1].writer
                            if writer is not None and writer.insn.name == 'MLOAD':
                                continue
                            growth_flag = True
                            break

                if growth_flag:
                    selected_traces.append(trace)

            loop.growth_traces[idx] = selected_traces
            idx += 1

    return loops


def get_traces_with_loop(cfg, ssa, loops) -> List:
    import networkx
    g = networkx.DiGraph()
    for bb in cfg.bbs:
        for succ in bb.succ:
            if bb.start < succ.start:
                g.add_edge(bb.start, succ.start)
    leaves = [v for v, d in g.out_degree() if d == 0]
    paths = list(networkx.all_simple_paths(g, cfg.root.start, leaves))
    
    traces = []
    for p in paths:
        if len([loop for loop in loops if loop.head in p]) == 0:
            continue
        
        path_blocks = [b for num in p for f in ssa.functions for b in f.blocks if num == b.offset]
        traces.append(path_blocks)
    
    # set function for loop    
    for loop in loops:
        for func in ssa.functions:
            if func.name in ['_fallthrough']:
                continue
            if func.offset in loop.bbs[0].ancestors:
                loop.function = func
                break

    return traces
