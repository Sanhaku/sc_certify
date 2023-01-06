from collections import defaultdict
from typing import DefaultDict, List
from src.loop import Loop

import src.rattle as rattle


def cal_iterate_times(functions_with_loop: DefaultDict[int, rattle.SSAFunction], loops: List[Loop], gas_limit=30_000_000):

    for loop in loops:
        # TODO: calculatre iterate_times for every loop
        loop.iterate_times = 0
