from src.rattle import ConcreteStackValue


def get_source(writer_insn, source, return_values):
    if writer_insn.return_value not in return_values:
        return_values.append(writer_insn.return_value)
    else:
        return
    if writer_insn.insn.name in ['SLOAD', 'CALLDATALOAD']:
        source.append(writer_insn)
        return
    if writer_insn.insn.name in ['MLOAD']:
        return

    if writer_insn.insn.name in ['PHI']:
        get_source(writer_insn.arguments[0].writer, source, return_values)
        get_source(writer_insn.arguments[1].writer, source, return_values)
        return

    if len(writer_insn.arguments) == 1:
        if not isinstance(writer_insn.arguments[0], ConcreteStackValue):
            get_source(writer_insn.arguments[0].writer, source, return_values)
    elif len(writer_insn.arguments) == 2:
        if not isinstance(writer_insn.arguments[0], ConcreteStackValue):
            get_source(writer_insn.arguments[0].writer, source, return_values)
        if not isinstance(writer_insn.arguments[1], ConcreteStackValue):
            get_source(writer_insn.arguments[1].writer, source, return_values)
    return
