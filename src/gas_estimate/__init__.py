from collections import defaultdict
from src.cfg.loop import Loop

import src.rattle as rattle


def cal_iterate_times(functions_with_loop: defaultdict(rattle.SSAFunction), loops: defaultdict(list(Loop)), gas_limit=30_000_000) -> dict:
    # TODO: calculatre iterate_times for every loop
    pass
