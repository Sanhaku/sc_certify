import sys

from collections import defaultdict
from typing import DefaultDict, List
from src.loop import Loop
from src.gas_estimate.exec import run_trace_has_loop_body, run_trace_has_head, run_trace_without_loop

class Func(object):
    def ___init_(self):
        self.has_loop = False
        self.loop = Loop()
        self.offset = 0
        self.base_gas = 0
        self.loop_gas_first = 0
        self.loop_gas_later = 0
        self.base_traces = []
        self.loop_trace = []

# filter out paths ending with illlegal opcode
def select_important_traces(key_traces: DefaultDict[int, List], loops: List[Loop]):
    traces = defaultdict(list)
    
    for index in key_traces:
      for trace in key_traces[index]:
        if trace[-1].ins[-1].name != 'INVALID' and trace[-1].ins[-1].name != 'REVERT':
            traces[index].append(trace)
    
    return traces 

# check one tarce: head or not, body or not, loop body list 
def check_trace(trace,loops):
    for loop in loops:
        # head_res = False
        # body_res = False
        for idx in range(len(trace) - len(loop.body) + 1):
            if trace[idx].start == loop.body[0]:
                for loop_idx in range(len(loop.body)):
                    if loop.body[loop_idx] != trace[idx+loop_idx].start:
                        return True, False, []
                return True, True, loop
    return False, False, []

# return certain function traces reuslts [list]
# 返回每条路径是否包含循环的情况(只有一个循环的情况)
def function_loop(traces: DefaultDict[int, List], function_label: int, loops: List[Loop]):
    func = []

    for trace in traces[function_label]:
        has_loop_head ,has_loop_body ,loop_body = check_trace(trace,loops)
        func.append([has_loop_head ,has_loop_body ,loop_body])
    return func

# return all function traces results
def all_funcs(traces: DefaultDict[int, List], loops: List[Loop]):
    funcs = defaultdict(list)
    for offset in traces:
        funcs[offset] = function_loop(traces,offset,loops)
    return funcs


# 执行所有函数、执行函数所有路径计算gas
def run_funcs_find_min(traces: DefaultDict[int, List], funcs: DefaultDict[int, List]):
    All_Funcs = defaultdict(Func)

    for offset in traces:
        func = Func()
        func.offset = offset
        min_loop_gas = sys.maxsize
        min_base_gas = sys.maxsize
        for idx in range(len(traces[offset])):
            if funcs[offset][idx][1]:
                func.has_loop = True
                # loopbody =  funcs[offset][idx][2]
                # loop_size = len(loopbody)
                cur_base_gas, cur_loop_gas_first, cur_loop_gas_later = run_trace_has_loop_body(traces[offset][idx], funcs[offset][idx][2])
                if cur_loop_gas_later < min_loop_gas:
                    func.loop_gas_first = cur_loop_gas_first
                    func.loop_gas_later = cur_loop_gas_later
                    func.loop_trace = traces[offset][idx]
                    func.loop = funcs[offset][idx][2]
            elif funcs[offset][idx][0]:
                cur_base_gas = run_trace_has_head(traces[offset][idx], funcs[offset][idx])
                if cur_base_gas < min_base_gas:
                    func.base_gas = cur_base_gas
                    func.base_traces = traces[offset][idx]       
            else:
                func.base_gas = run_trace_without_loop(traces[offset][idx], funcs[offset][idx])
        All_Funcs[offset] = func

    return All_Funcs;        

#
def calculate_max_times(all_fs: DefaultDict[int, Func],gas_limit):
    funcs_times = defaultdict(int)
    for offset in all_fs:
        if all_fs[offset].has_loop:
            max_time = (gas_limit - all_fs[offset].base_gas - all_fs[offset].loop_gas_first) / all_fs[offset].loop_gas_later + 1
            funcs_times[offset] = max_time
    return funcs_times
        

def bb_is_exist_in_loop(target_list, element):
    for line in target_list:
        if element.start in line.body:
            return True
    return False


def run_trace(trace:List, loops: List[Loop]):
    base_gas = 0
    loop_gas = 0
    for bb in trace:
        if bb_is_exist_in_loop(loops, bb):
            loop_gas += bb.static_gas
        else:
            base_gas += bb.static_gas
    return [base_gas,loop_gas]

def fun_run_gas(key_traces: DefaultDict[int, List], loops: List[Loop]):
    fun_gas = defaultdict(list)
    for func in key_traces:
        for trace in key_traces[func]:
            fun_gas[func].append(run_trace(trace,loops))
            
    return fun_gas









def find_max_gas_trace(key_traces: DefaultDict[int, List], function_label: int):
    function_traces = key_traces[function_label]

    max_gas = 0
    max_trace = defaultdict(list)

    for trace in function_label:
        cur_gas = run_max(trace)
      

def find_min_gas_trace(key_traces: DefaultDict[int, List], function_label: int):
    function_traces = key_traces[function_label]

    max_gas = 0
    max_trace = defaultdict(list)

    for trace in function_label:
      cur_gas = run_min(trace)

def run_max(trace):
    for bb in trace:
      bb.ins
    return 0

def run_min(trace):
    for bb in trace:
      bb.ins
    return 0



