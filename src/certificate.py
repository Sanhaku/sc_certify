from collections import defaultdict
from typing import List
from src.loop import Loop
from src.seq_generator import seq


class Certificate(object):
    def __init__(self, gas_limit=30_000_000, loops: List[Loop] = [], seq = None):
        self.gas_limit = gas_limit
        self.loops = []
        self.sequences = seq

    def __str__(self) -> str:
        s = f'gas limit: {self.gas_limit}\n\n'
        if not self.sequences:
            s += 'No vulnerabilities found\n'
            return s        
        for value in self.sequences.values():
            s += 'Unbounded loop in function: '
            func = value.func
            if func.name:
                s += func.name + '\n'
            else:
                s += f'_unknown_{func.hash:#x}()\n'
            
            s += f'Max Iterate times: {value.iterate_times}\n'    
            s += 'Execution trace: ['
            for block in value.growth_trace.analyzed_blocks:
                s += f'{block.block.offset:#x}, '
            s += ']\n'
            s += f'Execution times: {value.growth_times}\n\n'
        return s
