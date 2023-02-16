# schema: [opcode, ins, outs, gas]
# delete gas in next opcodes
opcodes = {
0x00: ['STOP', 0, 0],
    0x01: ['ADD', 2, 1],
    0x02: ['MUL', 2, 1],
    0x03: ['SUB', 2, 1],
    0x04: ['DIV', 2, 1],
    0x05: ['SDIV', 2, 1],
    0x06: ['MOD', 2, 1],
    0x07: ['SMOD', 2, 1],
    0x08: ['ADDMOD', 3, 1],
    0x09: ['MULMOD', 3, 1],
    0x0a: ['EXP', 2, 1],
    0x0b: ['SIGNEXTEND', 2, 1],
    0x10: ['LT', 2, 1],
    0x11: ['GT', 2, 1],
    0x12: ['SLT', 2, 1],
    0x13: ['SGT', 2, 1],
    0x14: ['EQ', 2, 1],
    0x15: ['ISZERO', 1, 1],
    0x16: ['AND', 2, 1],
    0x17: ['OR', 2, 1],
    0x18: ['XOR', 2, 1],
    0x19: ['NOT', 1, 1],
    0x1a: ['BYTE', 2, 1],
    0x1b: ['SHL', 2, 1],
    0x1c: ['SHR', 2, 1],
    0x1d: ['SAR', 2, 1],
    0x20: ['KECCAK256', 2, 1],
    0x30: ['ADDRESS', 0, 1],
    0x31: ['BALANCE', 1, 1],  # now 400
    0x32: ['ORIGIN', 0, 1],
    0x33: ['CALLER', 0, 1],
    0x34: ['CALLVALUE', 0, 1],
    0x35: ['CALLDATALOAD', 1, 1],
    0x36: ['CALLDATASIZE', 0, 1],
    0x37: ['CALLDATACOPY', 3, 0],
    0x38: ['CODESIZE', 0, 1],
    0x39: ['CODECOPY', 3, 0],
    0x3a: ['GASPRICE', 0, 1],
    0x3b: ['EXTCODESIZE', 1, 1],  # now 700
    0x3c: ['EXTCODECOPY', 4, 0],  # now 700
    0x3d: ['RETURNDATASIZE', 0, 1],
    0x3e: ['RETURNDATACOPY', 3, 0],
    0x40: ['BLOCKHASH', 1, 1],
    0x41: ['COINBASE', 0, 1],
    0x42: ['TIMESTAMP', 0, 1],
    0x43: ['NUMBER', 0, 1],
    0x44: ['DIFFICULTY', 0, 1],
    0x45: ['GASLIMIT', 0, 1],
    0x50: ['POP', 1, 0],
    0x51: ['MLOAD', 1, 1],
    0x52: ['MSTORE', 2, 0],
    0x53: ['MSTORE8', 2, 0],
    0x54: ['SLOAD', 1, 1],  # 200 now
    0x55: ['SSTORE', 2, 0],  # actual cost 5000-20000 depending on circumstance
    0x56: ['JUMP', 1, 0],
    0x57: ['JUMPI', 2, 0],
    0x58: ['PC', 0, 1],
    0x59: ['MSIZE', 0, 1],
    0x5a: ['GAS', 0, 1],
    0x5b: ['JUMPDEST', 0, 0],
    0xa0: ['LOG0', 2, 0],
    0xa1: ['LOG1', 3, 0],
    0xa2: ['LOG2', 4, 0],
    0xa3: ['LOG3', 5, 0],
    0xa4: ['LOG4', 6, 0],
    0xe1: ['SLOADBYTES', 3, 0],  # to be discontinued
    0xe2: ['SSTOREBYTES', 3, 0],  # to be discontinued
    0xe3: ['SSIZE', 1, 1],  # to be discontinued
    0xf0: ['CREATE', 3, 1],
    0xf1: ['CALL', 7, 1],  # 700 now
    0xf2: ['CALLCODE', 7, 1],  # 700 now
    0xf3: ['RETURN', 2, 0],
    0xf4: ['DELEGATECALL', 6, 1],  # 700 now
    0xf5: ['CALLBLACKBOX', 7, 1],
    0xfa: ['STATICCALL', 6, 1],
    0xfd: ['REVERT', 2, 0],
    0xfe: ['INVALID', 0, 0],
    0xff: ['SELFDESTRUCT', 1, 0],  # 5000 now
}

for i in range(1, 33):
    opcodes[0x5f + i] = ['PUSH' + str(i), 0, 1, 3]

for i in range(1, 17):
    opcodes[0x7f + i] = ['DUP' + str(i), i, i + 1, 3]
    opcodes[0x8f + i] = ['SWAP' + str(i), i + 1, i + 1, 3]

reverse_opcodes = {}
for o in opcodes:
    vars()[opcodes[o][0]] = opcodes[o]
    reverse_opcodes[opcodes[o][0]] = o

# According to EVM yellow paper

GCOST = {
    "Gzero": 0,
    "Gjumpdest": 1,
    "Gbase": 2,
    "Gverylow": 3,
    "Glow": 5,
    "Gmid": 8,
    "Ghigh": 10,
    "Gwarmaccess": 100,
    "Gaccesslistaddress": 2400,
    "Gaccessliststorage": 1900,
    "Gcoldaccountaccess": 2600,
    "Gcoldsload": 2100,
    "Gsset": 20000,
    "Gsreset": 2900,
    "Rsclear": 15000,
    "Rsuicide": 24000,
    "Gsuicide": 5000,
    "Gcreate": 32000,
    "Gcodedeposit": 200,
    # "Gcall": 34700,
    "Gcallvalue": 9000,
    "Gcallstipend": 2300,
    "Gnewaccount": 25000,
    "Gexp": 10,
    "Gexpbyte": 50,
    "Gmemory": 3,
    "Gtxcreate": 32000,
    "Gtxdatazero": 4,
    "Gtxdatanonzero": 16,
    "Gtransaction": 21000,
    "Glog": 375,
    "Glogdata": 8,
    "Glogtopic": 375,
    "Gsha3": 30,
    "Gsha3word": 6,
    "Gcopy": 3,
    "Gblockhash": 20
}

Wzero = ("STOP", "RETURN", "REVERT")

Wbase = ("ADDRESS", "ORIGIN", "CALLER", "CALLVALUE", "CALLDATASIZE",
         "CODESIZE", "GASPRICE", "COINBASE", "TIMESTAMP", "NUMBER",
         "DIFFICULTY", "GASLIMIT", "POP", "PC", "MSIZE", "GAS", "RETURNDATASIZE", "CHAINID")

Wverylow = ("ADD", "SUB", "NOT", "LT", "GT", "SLT", "SGT", "EQ",
            "ISZERO", "AND", "OR", "XOR", "BYTE", "CALLDATALOAD",
            "MLOAD", "MSTORE", "MSTORE8", "PUSH", "DUP", "SWAP", "SHL", "SHR", "SAR")

Wlow = ("MUL", "DIV", "SDIV", "MOD", "SMOD", "SIGNEXTEND", "SELFBALANCE")

Wmid = ("ADDMOD", "MULMOD", "JUMP")

Whigh = ("JUMPI")

Wcopy = ("CALLDATACOPY", "CODECOPY", "RETURNDATACOPY")

Wcall = ("CALL", "CALLCODE", "DELEGATECALL", "STATICCALL")

Wexaccount = ("BALANCE", "EXTCODESIZE", "EXTCODEHASH")

def get_ins_cost(opcode, params=None):
    if opcode in Wzero:
        return GCOST["Gzero"]
    elif opcode in Wbase:
        return GCOST["Gbase"]
    elif opcode in Wverylow or opcode.startswith("PUSH") or opcode.startswith("DUP") or opcode.startswith("SWAP"):
        return GCOST["Gverylow"]
    elif opcode in Wlow:
        return GCOST["Glow"]
    elif opcode in Wmid:
        return GCOST["Gmid"]
    elif opcode in Whigh:
        return GCOST["Ghigh"]
    elif opcode in Wcopy:
        return GCOST["Gcopy"]
    elif opcode in Wcall:
        return GCOST["Gcall"]
    elif opcode == "JUMPDEST":
        return GCOST["Gjumpdest"]
    elif opcode == "CREATE":
        return GCOST["Gcreate"]
    elif opcode == "CREATE2":
        return GCOST["Gcreate"]
    elif opcode in Wcall:
        return GCOST["Gcall"]
    elif opcode in ("LOG0", "LOG1", "LOG2", "LOG3", "LOG4"):
        num_topics = int(opcode[3:])
        return GCOST["Glog"] + num_topics * GCOST["Glogtopic"]
    elif opcode in Wcopy:
        return GCOST["Gcopy"]
    elif opcode in Wexaccount:
        return GCOST["Gblockhash"]
    elif opcode == "EXP":
        return 60
    elif opcode == "SHA3":
        return GCOST["Gsha3"]
    elif opcode == "KECCAK256":
        return GCOST["Gsha3"]
    elif opcode == "SLOAD":  # SLOAD's static gas is zero
        return 0
    elif opcode == "SSTORE":
        return 0
    return 0



# Non-opcode gas prices
# GDEFAULT = 1
# GMEMORY = 3
# GQUADRATICMEMDENOM = 512  # 1 gas per 512 quadwords
# GEXPONENTBYTE = 10  # cost of EXP exponent per byte
# GCOPY = 3  # cost to copy one 32 byte word
# GCONTRACTBYTE = 200  # one byte of code in contract creation
# GCALLVALUETRANSFER = 9000  # non-zero-valued call
# GLOGBYTE = 8  # cost of a byte of logdata

# GTXCOST = 21000  # TX BASE GAS COST
# GTXDATAZERO = 4  # TX DATA ZERO BYTE GAS COST
# GTXDATANONZERO = 68  # TX DATA NON ZERO BYTE GAS COST
# GSHA3WORD = 6  # Cost of SHA3 per word
# GSHA256BASE = 60  # Base c of SHA256
# GSHA256WORD = 12  # Cost of SHA256 per word
# GRIPEMD160BASE = 600  # Base cost of RIPEMD160
# GRIPEMD160WORD = 120  # Cost of RIPEMD160 per word
# GIDENTITYBASE = 15  # Base cost of indentity
# GIDENTITYWORD = 3  # Cost of identity per word
# GECRECOVER = 3000  # Cost of ecrecover op

# GSTIPEND = 2300

# GCALLNEWACCOUNT = 25000
# GSELFDESTRUCTREFUND = 24000

# GSTORAGEBASE = 2500
# GSTORAGEBYTESTORAGE = 250
# GSTORAGEBYTECHANGE = 40
# GSTORAGEMIN = 2500
# GSSIZE = 50
# GSLOADBYTES = 50

# GSTORAGEREFUND = 15000
# GSTORAGEKILL = 5000
# GSTORAGEMOD = 5000
# GSTORAGEADD = 20000

# GMODEXPQUADDIVISOR = 100
# GECADD = 500
# GECMUL = 2000

# GPAIRINGBASE = 100000
# GPAIRINGPERPOINT = 80000

# EXP_SUPPLEMENTAL_GAS = 40

# # Anti-DoS HF changes
# SLOAD_SUPPLEMENTAL_GAS = 150
# CALL_SUPPLEMENTAL_GAS = 660
# EXTCODELOAD_SUPPLEMENTAL_GAS = 680
# BALANCE_SUPPLEMENTAL_GAS = 380
# CALL_CHILD_LIMIT_NUM = 63
# CALL_CHILD_LIMIT_DENOM = 64
# SELFDESTRUCT_SUPPLEMENTAL_GAS = 5000

memory_writes = {'CALLDATACOPY': (-1, -3), 'CODECOPY': (-1, -3), 'EXTCODECOPY': (-2, -4), 'MSTORE': (-1, 32),
                 'MSTORE8': (-1, 8), 'CALL': (-6, -7), 'CALLCODE': (-6, -7), 'DELEGATECALL': (-5, -6)}
memory_reads = {'SHA3': (-1, -2), 'MLOAD': (-1, 32), 'CREATE': (-2, -3), 'CALL': (-4, -5), 'CALLCODE': (-4, -5),
                'RETURN': (-1, -2), 'DELEGATECALL': (-3, -4)}
storage_writes = {'SSTORE': -1}
storage_reads = {'SLOAD': -1}

potentially_user_controlled = ['ORIGIN', 'CALLER', 'CALLVALUE', 'CALLDATALOAD', 'CALLDATASIZE', 'CALLDATACOPY',
                               'EXTCODESIZE', 'EXTCODECOPY', 'SLOAD']

potentially_direct_user_controlled = ['ORIGIN', 'CALLER', 'CALLVALUE', 'CALLDATALOAD', 'CALLDATASIZE', 'CALLDATACOPY',
                               'EXTCODESIZE', 'EXTCODECOPY','SLOAD']

external_data = ['RETURNDATACOPY', 'RETURNDATASIZE', 'EXTCODESIZE', 'EXTCODECOPY']

CRITICAL = ['CALL', 'DELEGATECALL', 'CALLCODE', 'SELFDESTRUCT']

# map denoting attacker controlled stack arguments
CRITICAL_ARGS = {
    'CALL': [1],
    'DELEGATECALL': [1],
    'CALLCODE': [1],
    'SELFDESTRUCT': [0],
    'JUMPI': [1],
    'ISZERO': [0],
    'GT':[0,1],
    'LT':[0,1]
}
