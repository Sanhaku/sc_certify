import datetime
import logging
from collections import defaultdict
from typing import DefaultDict, List

from src.cfg.evm.exceptions import ExternalData, SymbolicError, IntractablePath, VMException
from src.cfg.util.utils import to_signed, TT256, TT256M1, bytearray_to_bytestr, big_endian_to_int, sha3, bytearray_to_int, bytes_to_int, encode_int32
from src.loop import Loop
from src.gas_estimate.state import Stack, Memory

class Context(object):
    def ___init_(self):
        self.address = 0
        self.balance = dict()
        self.origin = 0
        self.caller = 0
        self.callvalue = 0
        self.calldata = []
        self.gasprice = 0
        self.coinbase = 0
        self.timestamp = 0
        self.number = 0
        self.difficulty = 0
        self.gaslimit = 0
        self.storage = defaultdict(int)

class AccessSets(object):
    def __init__(self):
        self.address = dict
        self.slots = defaultdict(int)

def has_loop(trace, loops: List[Loop]):
    for bb in trace:
        for loop in loops:
            if bb.start == loop[0]:
                return True
    return False

def bb_is_exist_in_loop(target_list, element):
    for line in target_list:
        if element in line:
            return True
    return False



def run_trace_has_loop_body(trace,loop):
    aset = AccessSets()
    stk = Stack()
    mem = Memory()
    sto = defaultdict(int)
    ctx = Context()
    base_gas = 0
    loop_gas_first = 0
    loop_gas_later = 0
    

    for bb in trace:
        dynamic_gas = 0
        for ins in bb.ins:
            opcode = ins.op
            op = ins.name
            if 0x60 <= opcode <= 0x7f:
                stk.append(int.from_bytes(ins.arg, byteorder='big'))
            # Arithmetic
            # elif opcode < 0x10:
            #     if op == 'STOP':
            #         success = True
            #     elif op == 'ADD':
            #         stk.append(stk.pop() + stk.pop())
            #     elif op == 'SUB':
            #         stk.append(stk.pop() - stk.pop())
            #     elif op == 'MUL':
            #         stk.append(stk.pop() * stk.pop())
            #     elif op == 'DIV':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 // s1)
            #     elif op == 'MOD':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 % s1)
            #     elif op == 'SDIV':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) // abs(s1) *
            #                                  (-1 if s0 * s1 < 0 else 1))
            #     elif op == 'SMOD':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) % abs(s1) *
            #                                  (-1 if s0 < 0 else 1))
            #     elif op == 'ADDMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 + s1) % s2 if s2 else 0)
            #     elif op == 'MULMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 * s1) % s2 if s2 else 0)
            #     elif op == 'EXP':
            #         base, exponent = stk.pop(), stk.pop()
            #         stk.append(pow(base, exponent, TT256))
            #     elif op == 'SIGNEXTEND':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 <= 31:
            #             testbit = s0 * 8 + 7
            #             if s1 & (1 << testbit):
            #                 stk.append(s1 | (TT256 - (1 << testbit)))
            #             else:
            #                 stk.append(s1 & ((1 << testbit) - 1))
            #         else:
            #             stk.append(s1)
            # # Comparisons
            # elif opcode < 0x20:
            #     if op == 'LT':
            #         stk.append(1 if stk.pop() < stk.pop() else 0)
            #     elif op == 'GT':
            #         stk.append(1 if stk.pop() > stk.pop() else 0)
            #     elif op == 'SLT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 < s1 else 0)
            #     elif op == 'SGT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 > s1 else 0)
            #     elif op == 'EQ':
            #         stk.append(1 if stk.pop() == stk.pop() else 0)
            #     elif op == 'ISZERO':
            #         stk.append(0 if stk.pop() else 1)
            #     elif op == 'AND':
            #         stk.append(stk.pop() & stk.pop())
            #     elif op == 'OR':
            #         stk.append(stk.pop() | stk.pop())
            #     elif op == 'XOR':
            #         stk.append(stk.pop() ^ stk.pop())
            #     elif op == 'NOT':
            #         stk.append(TT256M1 - stk.pop())
            #     elif op == 'BYTE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 >= 32:
            #             stk.append(0)
            #         else:
            #             stk.append((s1 // 256 ** (31 - s0)) % 256)
            #     elif op == 'SHL':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 << s0))
            #     elif op == 'SHR':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 >> s0))
            #     elif op == 'SAR':
            #         s0, s1 = stk.pop(), to_signed(stk.pop())
            #         stk.append((s1 >> s0))
            # # SHA3 and environment info
            # elif opcode < 0x40:
            #     if op == 'SHA3':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, s1)
            #         data = bytearray_to_bytestr(mem[s0: s0 + s1])
            #         stk.append(big_endian_to_int(sha3(data)))
            #     elif op == 'ADDRESS':
            #         stk.append(ctx.address)
            #     elif op == 'BALANCE':
            #         s0 = stk.pop()
            #         if s0 not in ctx.balance:
            #             raise ExternalData('BALANCE')
            #         stk.append(ctx.balance[s0])
            #     elif op == 'ORIGIN':
            #         stk.append(ctx.origin)
            #     elif op == 'CALLER':
            #         stk.append(ctx.caller)
            #     elif op == 'CALLVALUE':
            #         stk.append(ctx.callvalue)
            #     elif op == 'CALLDATALOAD':
            #         s0 = stk.pop()
            #         ctx.calldata[s0:s0 + 32]=bytes([0]) *(31)+ b'\x20'                                     
            #         stk.append(bytearray_to_int(ctx.calldata[s0:s0 + 32]))
            #     elif op == 'CALLDATASIZE':
            #         stk.append(len(ctx.calldata))
            #     elif op == 'CALLDATACOPY':
            #         mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #         mem.extend(mstart, size)
            #         for i in range(size):
            #             if dstart + i < len(ctx.calldata):
            #                 mem[mstart + i] = ctx.calldata[dstart + i]
            #             else:
            #                 mem[mstart + i] = 0
            #     # elif op == 'CODESIZE':
            #     #     stk.append(len(code))
            #     # elif op == 'CODECOPY':
            #     #     mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #     #     mem.extend(mstart, size)
            #     #     for i in range(size):
            #     #         if dstart + i < len(code):
            #     #             mem[mstart + i] = code[dstart + i]
            #     #         else:
            #     #             mem[mstart + i] = 0
            #     elif op == 'RETURNDATACOPY':
            #         raise ExternalData('RETURNDATACOPY')
            #     elif op == 'RETURNDATASIZE':
            #         raise ExternalData('RETURNDATASIZE')
            #     elif op == 'GASPRICE':
            #         stk.append(ctx.gasprice)
            #     elif op == 'EXTCODESIZE':
            #         raise ExternalData('EXTCODESIZE')
            #     elif op == 'EXTCODECOPY':
            #         raise ExternalData('EXTCODECOPY')
            # # Block info
            # elif opcode < 0x50:
            #     if op == 'BLOCKHASH':
            #         raise ExternalData('BLOCKHASH')
            #     elif op == 'COINBASE':
            #         stk.append(ctx.coinbase)
            #     elif op == 'TIMESTAMP':
            #         stk.append(ctx.timestamp)
            #     elif op == 'NUMBER':
            #         stk.append(ctx.number)
            #     elif op == 'DIFFICULTY':
            #         stk.append(ctx.difficulty)
            #     elif op == 'GASLIMIT':
            #         stk.append(ctx.gaslimit)
            # # VM state manipulations
            # elif opcode < 0x60:
            #     if op == 'POP':
            #         stk.pop()
            #     elif op == 'MLOAD':
            #         s0 = stk.pop()
            #         mem.extend(s0, 32)
            #         stk.append(bytes_to_int(mem[s0: s0 + 32]))
            #     elif op == 'MSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 32)
            #         mem[s0: s0 + 32] = encode_int32(s1)
            #     elif op == 'MSTORE8':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 1)
            #         mem[s0] = s1 % 256
            #     elif op == 'SLOAD':
            #         s0 = stk.pop()
            #         stk.append(sto[s0])
            #     elif op == 'SSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         sto[s0] = s1
            #     elif op == 'JUMP':
            #         stk.pop()
            #         # state.pc = stk.pop()
            #         # if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #     raise VMException('BAD JUMPDEST')
            #         # continue
            #     elif op == 'JUMPI':
            #         s0, s1 = stk.pop(), stk.pop()
            #         # if s1:
            #         #     state.pc = s0
            #         #     if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #         raise VMException('BAD JUMPDEST')
            #         #     continue
            #     # elif op == 'PC':
            #     #     stk.append(pc)
            #     elif op == 'MSIZE':
            #         stk.append(len(mem))
            #     # elif op == 'GAS':
            #     #     stk.append(gas)
            # # DUPn (eg. DUP1: a b c -> a b c c, DUP3: a b c -> a b c a)
            # elif op[:3] == 'DUP':
            #     stk.append(stk[0x7f - opcode])  # 0x7f - opcode is a negative number, -1 for 0x80 ... -16 for 0x8f
            # # SWAPn (eg. SWAP1: a b c d -> a b d c, SWAP3: a b c d -> d b c a)
            # elif op[:4] == 'SWAP':
            # # 0x8e - opcode is a negative number, -2 for 0x90 ... -17 for 0x9f
            #     stk[-1], stk[0x8e - opcode] = stk[0x8e - opcode], stk[-1]
            # # Logs (aka "events")
            # elif op[:3] == 'LOG':
            #     depth = int(op[3:])
            #     mstart, msz = stk.pop(), stk.pop()
            #     topics = [stk.pop() for _ in range(depth)]
            #     mem.extend(mstart, msz)
            #     # Ignore external effects...
            # # Create a new contract
            # elif op == 'CREATE':
            #     raise ExternalData('CREATE')
            # # Calls
            # elif op in ('CALL', 'CALLCODE', 'DELEGATECALL', 'STATICCALL'):
            #     raise ExternalData(op)
            # # Return opcode
            # elif op == 'RETURN':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            #     success = True
            # # Revert opcode (Metropolis)
            # elif op == 'REVERT':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            # # SELFDESTRUCT opcode (also called SELFDESTRUCT)
            # elif op == 'SELFDESTRUCT':
                # raise ExternalData('SELFDESTRUCT')
        if bb.start in loop.body:
            loop_gas_first += bb.static_gas + dynamic_gas
        else:
            base_gas += bb.static_gas + dynamic_gas

    for bb in trace[(len(trace)-len(loop.body)):]:
        dynamic_gas = 0
        for ins in bb.ins:
            opcode = ins.op
            op = ins.name
            if 0x60 <= opcode <= 0x7f:
                stk.append(int.from_bytes(ins.arg, byteorder='big'))
            # Arithmetic
            # elif opcode < 0x10:
            #     if op == 'STOP':
            #         success = True
            #     elif op == 'ADD':
            #         stk.append(stk.pop() + stk.pop())
            #     elif op == 'SUB':
            #         stk.append(stk.pop() - stk.pop())
            #     elif op == 'MUL':
            #         stk.append(stk.pop() * stk.pop())
            #     elif op == 'DIV':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 // s1)
            #     elif op == 'MOD':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 % s1)
            #     elif op == 'SDIV':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) // abs(s1) *
            #                                  (-1 if s0 * s1 < 0 else 1))
            #     elif op == 'SMOD':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) % abs(s1) *
            #                                  (-1 if s0 < 0 else 1))
            #     elif op == 'ADDMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 + s1) % s2 if s2 else 0)
            #     elif op == 'MULMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 * s1) % s2 if s2 else 0)
            #     elif op == 'EXP':
            #         base, exponent = stk.pop(), stk.pop()
            #         stk.append(pow(base, exponent, TT256))
            #     elif op == 'SIGNEXTEND':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 <= 31:
            #             testbit = s0 * 8 + 7
            #             if s1 & (1 << testbit):
            #                 stk.append(s1 | (TT256 - (1 << testbit)))
            #             else:
            #                 stk.append(s1 & ((1 << testbit) - 1))
            #         else:
            #             stk.append(s1)
            # # Comparisons
            # elif opcode < 0x20:
            #     if op == 'LT':
            #         stk.append(1 if stk.pop() < stk.pop() else 0)
            #     elif op == 'GT':
            #         stk.append(1 if stk.pop() > stk.pop() else 0)
            #     elif op == 'SLT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 < s1 else 0)
            #     elif op == 'SGT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 > s1 else 0)
            #     elif op == 'EQ':
            #         stk.append(1 if stk.pop() == stk.pop() else 0)
            #     elif op == 'ISZERO':
            #         stk.append(0 if stk.pop() else 1)
            #     elif op == 'AND':
            #         stk.append(stk.pop() & stk.pop())
            #     elif op == 'OR':
            #         stk.append(stk.pop() | stk.pop())
            #     elif op == 'XOR':
            #         stk.append(stk.pop() ^ stk.pop())
            #     elif op == 'NOT':
            #         stk.append(TT256M1 - stk.pop())
            #     elif op == 'BYTE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 >= 32:
            #             stk.append(0)
            #         else:
            #             stk.append((s1 // 256 ** (31 - s0)) % 256)
            #     elif op == 'SHL':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 << s0))
            #     elif op == 'SHR':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 >> s0))
            #     elif op == 'SAR':
            #         s0, s1 = stk.pop(), to_signed(stk.pop())
            #         stk.append((s1 >> s0))
            # # SHA3 and environment info
            # elif opcode < 0x40:
            #     if op == 'SHA3':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, s1)
            #         data = bytearray_to_bytestr(mem[s0: s0 + s1])
            #         stk.append(big_endian_to_int(sha3(data)))
            #     elif op == 'ADDRESS':
            #         stk.append(ctx.address)
            #     elif op == 'BALANCE':
            #         s0 = stk.pop()
            #         if s0 not in ctx.balance:
            #             raise ExternalData('BALANCE')
            #         stk.append(ctx.balance[s0])
            #     elif op == 'ORIGIN':
            #         stk.append(ctx.origin)
            #     elif op == 'CALLER':
            #         stk.append(ctx.caller)
            #     elif op == 'CALLVALUE':
            #         stk.append(ctx.callvalue)
            #     elif op == 'CALLDATALOAD':
            #         s0 = stk.pop()
            #         ctx.calldata[s0:s0 + 32]=bytes([0]) *(31)+ b'\x20'                                     
            #         stk.append(bytearray_to_int(ctx.calldata[s0:s0 + 32]))
            #     elif op == 'CALLDATASIZE':
            #         stk.append(len(ctx.calldata))
            #     elif op == 'CALLDATACOPY':
            #         mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #         mem.extend(mstart, size)
            #         for i in range(size):
            #             if dstart + i < len(ctx.calldata):
            #                 mem[mstart + i] = ctx.calldata[dstart + i]
            #             else:
            #                 mem[mstart + i] = 0
            #     # elif op == 'CODESIZE':
            #     #     stk.append(len(code))
            #     # elif op == 'CODECOPY':
            #     #     mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #     #     mem.extend(mstart, size)
            #     #     for i in range(size):
            #     #         if dstart + i < len(code):
            #     #             mem[mstart + i] = code[dstart + i]
            #     #         else:
            #     #             mem[mstart + i] = 0
            #     elif op == 'RETURNDATACOPY':
            #         raise ExternalData('RETURNDATACOPY')
            #     elif op == 'RETURNDATASIZE':
            #         raise ExternalData('RETURNDATASIZE')
            #     elif op == 'GASPRICE':
            #         stk.append(ctx.gasprice)
            #     elif op == 'EXTCODESIZE':
            #         raise ExternalData('EXTCODESIZE')
            #     elif op == 'EXTCODECOPY':
            #         raise ExternalData('EXTCODECOPY')
            # # Block info
            # elif opcode < 0x50:
            #     if op == 'BLOCKHASH':
            #         raise ExternalData('BLOCKHASH')
            #     elif op == 'COINBASE':
            #         stk.append(ctx.coinbase)
            #     elif op == 'TIMESTAMP':
            #         stk.append(ctx.timestamp)
            #     elif op == 'NUMBER':
            #         stk.append(ctx.number)
            #     elif op == 'DIFFICULTY':
            #         stk.append(ctx.difficulty)
            #     elif op == 'GASLIMIT':
            #         stk.append(ctx.gaslimit)
            # # VM state manipulations
            # elif opcode < 0x60:
            #     if op == 'POP':
            #         stk.pop()
            #     elif op == 'MLOAD':
            #         s0 = stk.pop()
            #         mem.extend(s0, 32)
            #         stk.append(bytes_to_int(mem[s0: s0 + 32]))
            #     elif op == 'MSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 32)
            #         mem[s0: s0 + 32] = encode_int32(s1)
            #     elif op == 'MSTORE8':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 1)
            #         mem[s0] = s1 % 256
            #     elif op == 'SLOAD':
            #         s0 = stk.pop()
            #         stk.append(sto[s0])
            #     elif op == 'SSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         sto[s0] = s1
            #     elif op == 'JUMP':
            #         stk.pop()
            #         # state.pc = stk.pop()
            #         # if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #     raise VMException('BAD JUMPDEST')
            #         # continue
            #     elif op == 'JUMPI':
            #         s0, s1 = stk.pop(), stk.pop()
            #         # if s1:
            #         #     state.pc = s0
            #         #     if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #         raise VMException('BAD JUMPDEST')
            #         #     continue
            #     # elif op == 'PC':
            #     #     stk.append(pc)
            #     elif op == 'MSIZE':
            #         stk.append(len(mem))
            #     # elif op == 'GAS':
            #     #     stk.append(gas)
            # # DUPn (eg. DUP1: a b c -> a b c c, DUP3: a b c -> a b c a)
            # elif op[:3] == 'DUP':
            #     stk.append(stk[0x7f - opcode])  # 0x7f - opcode is a negative number, -1 for 0x80 ... -16 for 0x8f
            # # SWAPn (eg. SWAP1: a b c d -> a b d c, SWAP3: a b c d -> d b c a)
            # elif op[:4] == 'SWAP':
            # # 0x8e - opcode is a negative number, -2 for 0x90 ... -17 for 0x9f
            #     stk[-1], stk[0x8e - opcode] = stk[0x8e - opcode], stk[-1]
            # # Logs (aka "events")
            # elif op[:3] == 'LOG':
            #     depth = int(op[3:])
            #     mstart, msz = stk.pop(), stk.pop()
            #     topics = [stk.pop() for _ in range(depth)]
            #     mem.extend(mstart, msz)
            #     # Ignore external effects...
            # # Create a new contract
            # elif op == 'CREATE':
            #     raise ExternalData('CREATE')
            # # Calls
            # elif op in ('CALL', 'CALLCODE', 'DELEGATECALL', 'STATICCALL'):
            #     raise ExternalData(op)
            # # Return opcode
            # elif op == 'RETURN':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            #     success = True
            # # Revert opcode (Metropolis)
            # elif op == 'REVERT':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            # # SELFDESTRUCT opcode (also called SELFDESTRUCT)
            # elif op == 'SELFDESTRUCT':
            #     raise ExternalData('SELFDESTRUCT')
        loop_gas_later += bb.static_gas + dynamic_gas
    
    return base_gas, loop_gas_first, loop_gas_later


def run_trace_has_head(trace,loop):
    aset = AccessSets()
    stk = Stack()
    mem = Memory()
    sto = defaultdict(int)
    ctx = Context()
    base_gas = 0
    loop_gas_first = 0
    loop_gas_later = 0

    for bb in trace:
        dynamic_gas = 0
        for ins in bb.ins:
            opcode = ins.op
            op = ins.name
            if 0x60 <= opcode <= 0x7f:
                stk.append(int.from_bytes(ins.arg, byteorder='big'))
            # Arithmetic
            # elif opcode < 0x10:
            #     if op == 'STOP':
            #         success = True
            #     elif op == 'ADD':
            #         stk.append(stk.pop() + stk.pop())
            #     elif op == 'SUB':
            #         stk.append(stk.pop() - stk.pop())
            #     elif op == 'MUL':
            #         stk.append(stk.pop() * stk.pop())
            #     elif op == 'DIV':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 // s1)
            #     elif op == 'MOD':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 % s1)
            #     elif op == 'SDIV':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) // abs(s1) *
            #                                  (-1 if s0 * s1 < 0 else 1))
            #     elif op == 'SMOD':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) % abs(s1) *
            #                                  (-1 if s0 < 0 else 1))
            #     elif op == 'ADDMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 + s1) % s2 if s2 else 0)
            #     elif op == 'MULMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 * s1) % s2 if s2 else 0)
            #     elif op == 'EXP':
            #         base, exponent = stk.pop(), stk.pop()
            #         stk.append(pow(base, exponent, TT256))
            #     elif op == 'SIGNEXTEND':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 <= 31:
            #             testbit = s0 * 8 + 7
            #             if s1 & (1 << testbit):
            #                 stk.append(s1 | (TT256 - (1 << testbit)))
            #             else:
            #                 stk.append(s1 & ((1 << testbit) - 1))
            #         else:
            #             stk.append(s1)
            # # Comparisons
            # elif opcode < 0x20:
            #     if op == 'LT':
            #         stk.append(1 if stk.pop() < stk.pop() else 0)
            #     elif op == 'GT':
            #         stk.append(1 if stk.pop() > stk.pop() else 0)
            #     elif op == 'SLT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 < s1 else 0)
            #     elif op == 'SGT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 > s1 else 0)
            #     elif op == 'EQ':
            #         stk.append(1 if stk.pop() == stk.pop() else 0)
            #     elif op == 'ISZERO':
            #         stk.append(0 if stk.pop() else 1)
            #     elif op == 'AND':
            #         stk.append(stk.pop() & stk.pop())
            #     elif op == 'OR':
            #         stk.append(stk.pop() | stk.pop())
            #     elif op == 'XOR':
            #         stk.append(stk.pop() ^ stk.pop())
            #     elif op == 'NOT':
            #         stk.append(TT256M1 - stk.pop())
            #     elif op == 'BYTE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 >= 32:
            #             stk.append(0)
            #         else:
            #             stk.append((s1 // 256 ** (31 - s0)) % 256)
            #     elif op == 'SHL':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 << s0))
            #     elif op == 'SHR':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 >> s0))
            #     elif op == 'SAR':
            #         s0, s1 = stk.pop(), to_signed(stk.pop())
            #         stk.append((s1 >> s0))
            # # SHA3 and environment info
            # elif opcode < 0x40:
            #     if op == 'SHA3':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, s1)
            #         data = bytearray_to_bytestr(mem[s0: s0 + s1])
            #         stk.append(big_endian_to_int(sha3(data)))
            #     elif op == 'ADDRESS':
            #         stk.append(ctx.address)
            #     elif op == 'BALANCE':
            #         s0 = stk.pop()
            #         if s0 not in ctx.balance:
            #             raise ExternalData('BALANCE')
            #         stk.append(ctx.balance[s0])
            #     elif op == 'ORIGIN':
            #         stk.append(ctx.origin)
            #     elif op == 'CALLER':
            #         stk.append(ctx.caller)
            #     elif op == 'CALLVALUE':
            #         stk.append(ctx.callvalue)
            #     elif op == 'CALLDATALOAD':
            #         s0 = stk.pop()
            #         ctx.calldata[s0:s0 + 32]=bytes([0]) *(31)+ b'\x20'                                     
            #         stk.append(bytearray_to_int(ctx.calldata[s0:s0 + 32]))
            #     elif op == 'CALLDATASIZE':
            #         stk.append(len(ctx.calldata))
            #     elif op == 'CALLDATACOPY':
            #         mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #         mem.extend(mstart, size)
            #         for i in range(size):
            #             if dstart + i < len(ctx.calldata):
            #                 mem[mstart + i] = ctx.calldata[dstart + i]
            #             else:
            #                 mem[mstart + i] = 0
            #     # elif op == 'CODESIZE':
            #     #     stk.append(len(code))
            #     # elif op == 'CODECOPY':
            #     #     mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #     #     mem.extend(mstart, size)
            #     #     for i in range(size):
            #     #         if dstart + i < len(code):
            #     #             mem[mstart + i] = code[dstart + i]
            #     #         else:
            #     #             mem[mstart + i] = 0
            #     elif op == 'RETURNDATACOPY':
            #         raise ExternalData('RETURNDATACOPY')
            #     elif op == 'RETURNDATASIZE':
            #         raise ExternalData('RETURNDATASIZE')
            #     elif op == 'GASPRICE':
            #         stk.append(ctx.gasprice)
            #     elif op == 'EXTCODESIZE':
            #         raise ExternalData('EXTCODESIZE')
            #     elif op == 'EXTCODECOPY':
            #         raise ExternalData('EXTCODECOPY')
            # # Block info
            # elif opcode < 0x50:
            #     if op == 'BLOCKHASH':
            #         raise ExternalData('BLOCKHASH')
            #     elif op == 'COINBASE':
            #         stk.append(ctx.coinbase)
            #     elif op == 'TIMESTAMP':
            #         stk.append(ctx.timestamp)
            #     elif op == 'NUMBER':
            #         stk.append(ctx.number)
            #     elif op == 'DIFFICULTY':
            #         stk.append(ctx.difficulty)
            #     elif op == 'GASLIMIT':
            #         stk.append(ctx.gaslimit)
            # # VM state manipulations
            # elif opcode < 0x60:
            #     if op == 'POP':
            #         stk.pop()
            #     elif op == 'MLOAD':
            #         s0 = stk.pop()
            #         mem.extend(s0, 32)
            #         stk.append(bytes_to_int(mem[s0: s0 + 32]))
            #     elif op == 'MSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 32)
            #         mem[s0: s0 + 32] = encode_int32(s1)
            #     elif op == 'MSTORE8':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 1)
            #         mem[s0] = s1 % 256
            #     elif op == 'SLOAD':
            #         s0 = stk.pop()
            #         stk.append(sto[s0])
            #     elif op == 'SSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         sto[s0] = s1
            #     elif op == 'JUMP':
            #         stk.pop()
            #         # state.pc = stk.pop()
            #         # if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #     raise VMException('BAD JUMPDEST')
            #         # continue
            #     elif op == 'JUMPI':
            #         s0, s1 = stk.pop(), stk.pop()
            #         # if s1:
            #         #     state.pc = s0
            #         #     if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #         raise VMException('BAD JUMPDEST')
            #         #     continue
            #     # elif op == 'PC':
            #     #     stk.append(pc)
            #     elif op == 'MSIZE':
            #         stk.append(len(mem))
            #     # elif op == 'GAS':
            #     #     stk.append(gas)
            # # DUPn (eg. DUP1: a b c -> a b c c, DUP3: a b c -> a b c a)
            # elif op[:3] == 'DUP':
            #     stk.append(stk[0x7f - opcode])  # 0x7f - opcode is a negative number, -1 for 0x80 ... -16 for 0x8f
            # # SWAPn (eg. SWAP1: a b c d -> a b d c, SWAP3: a b c d -> d b c a)
            # elif op[:4] == 'SWAP':
            # # 0x8e - opcode is a negative number, -2 for 0x90 ... -17 for 0x9f
            #     stk[-1], stk[0x8e - opcode] = stk[0x8e - opcode], stk[-1]
            # # Logs (aka "events")
            # elif op[:3] == 'LOG':
            #     depth = int(op[3:])
            #     mstart, msz = stk.pop(), stk.pop()
            #     topics = [stk.pop() for _ in range(depth)]
            #     mem.extend(mstart, msz)
            #     # Ignore external effects...
            # # Create a new contract
            # elif op == 'CREATE':
            #     raise ExternalData('CREATE')
            # # Calls
            # elif op in ('CALL', 'CALLCODE', 'DELEGATECALL', 'STATICCALL'):
            #     raise ExternalData(op)
            # # Return opcode
            # elif op == 'RETURN':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            #     success = True
            # # Revert opcode (Metropolis)
            # elif op == 'REVERT':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            # # SELFDESTRUCT opcode (also called SELFDESTRUCT)
            # elif op == 'SELFDESTRUCT':
                # raise ExternalData('SELFDESTRUCT')
        base_gas += bb.static_gas + dynamic_gas

    return base_gas


def run_trace_without_loop(trace,loop):
    aset = AccessSets()
    stk = Stack()
    mem = Memory()
    sto = defaultdict(int)
    ctx = Context()
    base_gas = 0
    loop_gas_first = 0
    loop_gas_later = 0

    for bb in trace:
        dynamic_gas = 0
        for ins in bb.ins:
            opcode = ins.op
            op = ins.name
            if 0x60 <= opcode <= 0x7f:
                stk.append(int.from_bytes(ins.arg, byteorder='big'))
            # Arithmetic
            # elif opcode < 0x10:
            #     if op == 'STOP':
            #         success = True
            #     elif op == 'ADD':
            #         stk.append(stk.pop() + stk.pop())
            #     elif op == 'SUB':
            #         stk.append(stk.pop() - stk.pop())
            #     elif op == 'MUL':
            #         stk.append(stk.pop() * stk.pop())
            #     elif op == 'DIV':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 // s1)
            #     elif op == 'MOD':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append(0 if s1 == 0 else s0 % s1)
            #     elif op == 'SDIV':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) // abs(s1) *
            #                                  (-1 if s0 * s1 < 0 else 1))
            #     elif op == 'SMOD':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(0 if s1 == 0 else abs(s0) % abs(s1) *
            #                                  (-1 if s0 < 0 else 1))
            #     elif op == 'ADDMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 + s1) % s2 if s2 else 0)
            #     elif op == 'MULMOD':
            #         s0, s1, s2 = stk.pop(), stk.pop(), stk.pop()
            #         stk.append((s0 * s1) % s2 if s2 else 0)
            #     elif op == 'EXP':
            #         base, exponent = stk.pop(), stk.pop()
            #         stk.append(pow(base, exponent, TT256))
            #     elif op == 'SIGNEXTEND':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 <= 31:
            #             testbit = s0 * 8 + 7
            #             if s1 & (1 << testbit):
            #                 stk.append(s1 | (TT256 - (1 << testbit)))
            #             else:
            #                 stk.append(s1 & ((1 << testbit) - 1))
            #         else:
            #             stk.append(s1)
            # # Comparisons
            # elif opcode < 0x20:
            #     if op == 'LT':
            #         stk.append(1 if stk.pop() < stk.pop() else 0)
            #     elif op == 'GT':
            #         stk.append(1 if stk.pop() > stk.pop() else 0)
            #     elif op == 'SLT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 < s1 else 0)
            #     elif op == 'SGT':
            #         s0, s1 = to_signed(stk.pop()), to_signed(stk.pop())
            #         stk.append(1 if s0 > s1 else 0)
            #     elif op == 'EQ':
            #         stk.append(1 if stk.pop() == stk.pop() else 0)
            #     elif op == 'ISZERO':
            #         stk.append(0 if stk.pop() else 1)
            #     elif op == 'AND':
            #         stk.append(stk.pop() & stk.pop())
            #     elif op == 'OR':
            #         stk.append(stk.pop() | stk.pop())
            #     elif op == 'XOR':
            #         stk.append(stk.pop() ^ stk.pop())
            #     elif op == 'NOT':
            #         stk.append(TT256M1 - stk.pop())
            #     elif op == 'BYTE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         if s0 >= 32:
            #             stk.append(0)
            #         else:
            #             stk.append((s1 // 256 ** (31 - s0)) % 256)
            #     elif op == 'SHL':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 << s0))
            #     elif op == 'SHR':
            #         s0, s1 = stk.pop(), stk.pop()
            #         stk.append((s1 >> s0))
            #     elif op == 'SAR':
            #         s0, s1 = stk.pop(), to_signed(stk.pop())
            #         stk.append((s1 >> s0))
            # # SHA3 and environment info
            # elif opcode < 0x40:
            #     if op == 'SHA3':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, s1)
            #         data = bytearray_to_bytestr(mem[s0: s0 + s1])
            #         stk.append(big_endian_to_int(sha3(data)))
            #     elif op == 'ADDRESS':
            #         stk.append(ctx.address)
            #     elif op == 'BALANCE':
            #         s0 = stk.pop()
            #         if s0 not in ctx.balance:
            #             raise ExternalData('BALANCE')
            #         stk.append(ctx.balance[s0])
            #     elif op == 'ORIGIN':
            #         stk.append(ctx.origin)
            #     elif op == 'CALLER':
            #         stk.append(ctx.caller)
            #     elif op == 'CALLVALUE':
            #         stk.append(ctx.callvalue)
            #     elif op == 'CALLDATALOAD':
            #         s0 = stk.pop()
            #         #ctx.calldata[s0:s0 + 32]=bytes([0]) *(31)+ b'\x20'                                     
            #         stk.append(bytearray_to_int(ctx.calldata[s0:s0 + 32]))
            #     elif op == 'CALLDATASIZE':
            #         stk.append(len(ctx.calldata))
            #     elif op == 'CALLDATACOPY':
            #         mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #         mem.extend(mstart, size)
            #         for i in range(size):
            #             if dstart + i < len(ctx.calldata):
            #                 mem[mstart + i] = ctx.calldata[dstart + i]
            #             else:
            #                 mem[mstart + i] = 0
            #     # elif op == 'CODESIZE':
            #     #     stk.append(len(code))
            #     # elif op == 'CODECOPY':
            #     #     mstart, dstart, size = stk.pop(), stk.pop(), stk.pop()
            #     #     mem.extend(mstart, size)
            #     #     for i in range(size):
            #     #         if dstart + i < len(code):
            #     #             mem[mstart + i] = code[dstart + i]
            #     #         else:
            #     #             mem[mstart + i] = 0
            #     elif op == 'RETURNDATACOPY':
            #         raise ExternalData('RETURNDATACOPY')
            #     elif op == 'RETURNDATASIZE':
            #         raise ExternalData('RETURNDATASIZE')
            #     elif op == 'GASPRICE':
            #         stk.append(ctx.gasprice)
            #     elif op == 'EXTCODESIZE':
            #         raise ExternalData('EXTCODESIZE')
            #     elif op == 'EXTCODECOPY':
            #         raise ExternalData('EXTCODECOPY')
            # # Block info
            # elif opcode < 0x50:
            #     if op == 'BLOCKHASH':
            #         raise ExternalData('BLOCKHASH')
            #     elif op == 'COINBASE':
            #         stk.append(ctx.coinbase)
            #     elif op == 'TIMESTAMP':
            #         stk.append(ctx.timestamp)
            #     elif op == 'NUMBER':
            #         stk.append(ctx.number)
            #     elif op == 'DIFFICULTY':
            #         stk.append(ctx.difficulty)
            #     elif op == 'GASLIMIT':
            #         stk.append(ctx.gaslimit)
            # # VM state manipulations
            # elif opcode < 0x60:
            #     if op == 'POP':
            #         stk.pop()
            #     elif op == 'MLOAD':
            #         s0 = stk.pop()
            #         mem.extend(s0, 32)
            #         stk.append(bytes_to_int(mem[s0: s0 + 32]))
            #     elif op == 'MSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 32)
            #         mem[s0: s0 + 32] = encode_int32(s1)
            #     elif op == 'MSTORE8':
            #         s0, s1 = stk.pop(), stk.pop()
            #         mem.extend(s0, 1)
            #         mem[s0] = s1 % 256
            #     elif op == 'SLOAD':
            #         s0 = stk.pop()
            #         stk.append(sto[s0])
            #     elif op == 'SSTORE':
            #         s0, s1 = stk.pop(), stk.pop()
            #         sto[s0] = s1
            #     elif op == 'JUMP':
            #         stk.pop()
            #         # state.pc = stk.pop()
            #         # if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #     raise VMException('BAD JUMPDEST')
            #         # continue
            #     elif op == 'JUMPI':
            #         s0, s1 = stk.pop(), stk.pop()
            #         # if s1:
            #         #     state.pc = s0
            #         #     if state.pc >= len(state.code) or not program[state.pc].name == 'JUMPDEST':
            #         #         raise VMException('BAD JUMPDEST')
            #         #     continue
            #     # elif op == 'PC':
            #     #     stk.append(pc)
            #     elif op == 'MSIZE':
            #         stk.append(len(mem))
            #     # elif op == 'GAS':
            #     #     stk.append(gas)
            # # DUPn (eg. DUP1: a b c -> a b c c, DUP3: a b c -> a b c a)
            # elif op[:3] == 'DUP':
            #     stk.append(stk[0x7f - opcode])  # 0x7f - opcode is a negative number, -1 for 0x80 ... -16 for 0x8f
            # # SWAPn (eg. SWAP1: a b c d -> a b d c, SWAP3: a b c d -> d b c a)
            # elif op[:4] == 'SWAP':
            # # 0x8e - opcode is a negative number, -2 for 0x90 ... -17 for 0x9f
            #     stk[-1], stk[0x8e - opcode] = stk[0x8e - opcode], stk[-1]
            # # Logs (aka "events")
            # elif op[:3] == 'LOG':
            #     depth = int(op[3:])
            #     mstart, msz = stk.pop(), stk.pop()
            #     topics = [stk.pop() for _ in range(depth)]
            #     mem.extend(mstart, msz)
            #     # Ignore external effects...
            # # Create a new contract
            # elif op == 'CREATE':
            #     raise ExternalData('CREATE')
            # # Calls
            # elif op in ('CALL', 'CALLCODE', 'DELEGATECALL', 'STATICCALL'):
            #     raise ExternalData(op)
            # # Return opcode
            # elif op == 'RETURN':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            #     success = True
            # # Revert opcode (Metropolis)
            # elif op == 'REVERT':
            #     s0, s1 = stk.pop(), stk.pop()
            #     mem.extend(s0, s1)
            # # SELFDESTRUCT opcode (also called SELFDESTRUCT)
            # elif op == 'SELFDESTRUCT':
            #     raise ExternalData('SELFDESTRUCT')
        base_gas += bb.static_gas + dynamic_gas

    return base_gas
