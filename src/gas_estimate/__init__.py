from collections import defaultdict
from typing import DefaultDict, List
from src.loop import Loop

import src.rattle as rattle

from src.gas_estimate.pre_process import select_important_traces, all_funcs,run_funcs_find_min, calculate_max_times


def cal_iterate_times(key_traces: DefaultDict[int, List], loops: List[Loop], gas_limit=30_000_000):

    select_traces = select_important_traces(key_traces, loops)
    funcs = all_funcs(select_traces,loops)
    all_f = run_funcs_find_min(select_traces,funcs)

    # TODO: calculatre iterate_times for every function
    func_iterate_time = calculate_max_times(all_f, gas_limit)

    return func_iterate_time
