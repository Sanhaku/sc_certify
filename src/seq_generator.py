import logging
from typing import List
from z3 import BitVec, Solver, sat, unsat
from src.loop import Loop
from src.rattle.ssa import ConcreteStackValue
from src.sym_exec.environment import Environment
from src.sym_exec.trace import Trace
from src.sym_exec.instructions import instructions_functions
from src.sym_exec.utils import WORD_SIZE

logger = logging.getLogger(__name__)


class SeqGenerator(object):
    def __init__(self, ssa, loops: List[Loop], key_traces: List, func_iterate_times):
        self.ssa = ssa
        self.loops = loops
        self.key_traces = key_traces
        self.func_iterate_times = func_iterate_times
        self.exec_seq = dict()

    def execute(self, timeout=300_000):
        # find a transaction sequence that will make the loop iterate iterate_times

        for loop in self.loops:
            if len(loop.key_variable) == 0:
                logger.error(
                    f"Key variable not found in {loop}")
                continue

            # solve the constraints when loop iterates max times
            if self.__solve_loop_iterates(loop, timeout) == unsat:
                continue

            # verify the reachability of a certain contract state
            self.__solve_reachability(loop, timeout)
        return self.exec_seq

    def __solve_loop_iterates(self, loop, timeout):
        loop_body = [
            b for num in loop.body for f in self.ssa.functions for b in f.blocks if num == b.offset]
        if len(loop_body) == 0:
            logger.error(f"Loop body not found in {loop}")
            raise Exception

        for key_trace in self.key_traces:
            if len([b for b in key_trace if loop.head == b.offset]) == 0:
                continue

            # expand loop
            if loop_body[0] not in key_trace:
                continue
            head_idx = key_trace.index(loop_body[0])
            blocks = key_trace[:head_idx]

            iterate_times = int(self.func_iterate_times[loop.function.offset])
            for i in range(iterate_times):
                blocks.extend(loop_body)
            blocks.extend(key_trace[head_idx:])

            constraints = self.__sym_exec_blocks(blocks)
            s = Solver()
            s.set('timeout', timeout)
            s.add(constraints)
            if s.check() == sat:
                return sat
        return unsat

    def __solve_reachability(self, loop, timeout):
        iterate_times = int(self.func_iterate_times[loop.function.offset])
        for v_idx, key_variable in enumerate(loop.key_variable):
            if key_variable.insn.name == "SLOAD":
                # key variable is a global variable
                key_expr = self.__to_z3_expr(key_variable)
                # TODO: set initial value for key variable
                key_expr = 0
                # calculate the final state of the key variable
                final_value = self.__get_final_state(loop, iterate_times)

                growth_traces = loop.growth_traces[v_idx]
                if len(growth_traces) == 0:
                    continue
                for trace in growth_traces:
                    # calculate growth times
                    growth_times = final_value - key_expr
                    constraints = []
                    # TODO: change variables when executing each trace
                    for i in range(growth_times):
                        constraints.extend(trace.constraints)

                    constraints.append(key_expr > final_value)
                    s = Solver()
                    s.set('timeout', timeout)
                    s.add(constraints)
                    if s.check() == sat:
                        func = loop.function
                        if func is not None:
                            self.exec_seq[func.offset] = seq(
                                trace, growth_times, func, iterate_times)
                            return sat
                        else:
                            logger.error(
                                f"Instruction of key variable type error")
                            raise Exception

            elif key_variable.insn.name == "CALLDATALOAD":
                # TODO: key variable is from user input
                func = loop.function
                if func is not None:
                    self.exec_seq[func.offset] = seq()
                    return sat
                else:
                    logger.error(
                        f"Instruction of key variable type error")
                    raise Exception
            else:
                logger.error(
                    f"Instruction of key variable type error")
                raise Exception

        return unsat

    def __sym_exec_blocks(self, blocks):
        trace = Trace(environment=Environment(self.ssa.internal.filedata))
        constraints = []
        for block in blocks:
            to_analyse = []
            for instruction in block.insns:
                if instruction.insn.is_push:
                    mnemonic = 'PUSH'
                else:
                    mnemonic = instruction.insn.mnemonic
                func = instructions_functions.get(mnemonic, None)
                if func is None:
                    logger.error(f"Instruction {mnemonic} is not implemented.")
                    raise NotImplementedError
                rv = func(instruction, trace.state)
                if rv is not None:
                    for t in rv:
                        if len(t) < 2:
                            logger.error(f"Instruction return value error")
                            raise Exception
                        else:
                            if t[0] in blocks and t[1] is not None:
                                constraints.append(t[1])

        return constraints

    def __get_final_state(self, loop, iterate_times):
        loop_body = [
            b for num in loop.body for f in self.ssa.functions for b in f.blocks if num == b.offset]
        loop_head = loop_body[0]

        induction_insn = None
        # find induction variable
        if len(loop_head.insns) < 2 or loop_head.insns[-2].insn.name != 'ISZERO':
            logger.error(f"loop head not found")
            raise Exception
        condition_insn = loop_head.insns[-2].arguments[0].writer
        initial_value = None
        for con_arg in condition_insn.arguments:
            phi_insn = con_arg.writer
            if phi_insn is None or phi_insn.insn.name != 'PHI':
                continue

            induction_arg = [
                phi_arg for phi_arg in phi_insn.arguments for block in loop_body if phi_arg.writer in block.insns]
            if len(induction_arg) > 0:
                induction_insn = induction_arg[0].writer
                for arg in induction_insn.arguments:
                    if arg != induction_arg:
                        if arg.value != -1:
                            logger.error(
                                f"initial value of induction variable is not a concrete value")
                            raise Exception
                        initial_value = arg.concrete_value
                        break
                break

        if induction_insn is None:
            logger.error(f"induction variable not found")
            raise Exception

        if initial_value is None:
            logger.error(f"initial value of induction variable not found")
            raise Exception

        step = induction_insn.arguments[0]
        if step.value != -1:
            logger.error(
                f"arguments of induction_insn is not a concrete value")
            raise Exception
        if induction_insn.insn.name == 'ADD':
            return initial_value + step.concrete_value * iterate_times
        elif induction_insn.insn.name == 'SUB':
            return initial_value - step.concrete_value * iterate_times
        elif induction_insn.insn.name == 'MUL':
            return initial_value * (step.concrete_value ** iterate_times)
        elif induction_insn.insn.name == 'DIV':
            return initial_value / (step.concrete_value ** iterate_times)
        else:
            logger.error(
                f"induction_insn {induction_insn.insn.name} is not implemented")
            raise Exception

    def __to_z3_expr(self, instruction):
        # storage_0 & calldataload_0
        args = instruction.arguments
        args_len = len(args)
        if args_len != 1:
            logger.error(
                f"Instruction of key variable needs 1 argument but {args_len} was given")
            raise Exception

        arg = instruction.arguments[0]
        if isinstance(arg, ConcreteStackValue):
            key = arg.concrete_value
        else:
            logger.error(
                f"Argument of SLOAD instruction is not a concrete value")
            raise Exception

        if instruction.insn.name == "SLOAD":
            bv_name = f"storage_{str(key)}"
        elif instruction.insn.name == "CALLDATALOAD":
            bv_name = f"calldataload_{str(key)}"
        else:
            logger.error(
                f"Instruction of key variable type error")
            raise Exception
        return BitVec(bv_name, WORD_SIZE)


class seq(object):
    def __init__(self, growth_trace=None, growth_times=None, func=None, iterate_times=None):
        self.growth_trace = growth_trace
        self.growth_times = growth_times
        self.func = func
        self.iterate_times = iterate_times
