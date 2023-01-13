import argparse
import logging
import os
import subprocess
from src.rattle import Recover
from src.sym_exec.symbolic_executor import SymExec
from src.cfg.cfg import CFG
from src.cfg.disassembly import generate_BBs
import src.gas_estimate as GasEstimate
from src.seq_generator import SeqGenerator
from src.certificate import Certificate
from src.trace_filter import get_growth_traces

logger = logging.getLogger()


def main():
    default_max_depth = 25
    default_timeout = 300_000
    default_gas_limit = 30_000_000

    parser = argparse.ArgumentParser(description='demo')
    parser.add_argument('--file', '-f', type=str,
                        help='Evm bytecode source file.')
    parser.add_argument('--gas_limit', '-gl', type=int, default=default_gas_limit,
                        help=f'Total gas limit provided by all transactions in the block. Default = {default_gas_limit}')
    parser.add_argument('--max-depth', '-md', type=int, default=default_max_depth,
                        help=f'Max recursion depth. The counting is how many basic blocks should be analysed. Default = {default_max_depth}')
    parser.add_argument('--timeout', '-t', type=int, default=default_timeout,
                        help=f'Timeout to Z3 Solver. Default = {default_timeout}')
    args = parser.parse_args()

    with open(args.file) as infile:
        inbuffer = infile.read().rstrip()
    code = bytes.fromhex(inbuffer)

    try:
        analyze(code, args)
    except Exception as e:
        logger.exception(e)


def analyze(code, args):
    cfg = CFG(generate_BBs(code))
    # visualize_cfg(cfg)
    loops = cfg.find_loops()
    ssa = Recover(bytes.hex(code).encode(), edges=[], optimize=True)

    traces = SymExec(ssa, args.max_depth).execute()
    # print(f"Found {len(traces)} traces")
    for loop in loops:
        loop.find_key_variable(ssa)
    loops = list(filter(lambda x: x.key_variable is not None, loops))
    loops = get_growth_traces(traces, loops)

    functions_with_loop = cfg.find_functions_with_loop(ssa, loops)
    GasEstimate.cal_iterate_times(
        functions_with_loop, loops, args.gas_limit)

    SeqGenerator(loops).execute(args.timeout)

    print(Certificate(args.gas_limit, loops))


def visualize_cfg(cfg: CFG):
    if not os.path.exists('output'):
        os.makedirs('output')
    out_dot = 'output/cfg.dot'
    out_png = 'output/cfg.png'
    with open(out_dot, 'w') as f:
        f.write(cfg.to_dot())
    subprocess.call(['dot', '-Tpng', f'-o{out_png}', out_dot])


if __name__ == '__main__':
    main()
