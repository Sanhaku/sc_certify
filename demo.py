import argparse
import logging
import os
import subprocess
from src.rattle import Recover
from src.sym_exec.symbolic_executor import SymExec
from src.cfg.cfg import CFG
from src.cfg.disassembly import generate_BBs
from src.gas_estimate import cal_iterate_times
from src.analyze import Analyze
from src.certificate import Certificate

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
    functions_with_loop = cfg.find_functions_with_loop(ssa, loops)

    iterate_times = cal_iterate_times(
        functions_with_loop, loops, args.gas_limit)

    traces = SymExec(ssa, args.max_depth).execute()
    # print(f"Found {len(traces)} traces")
    analyze = Analyze(ssa, traces)
    key_variables = analyze.get_key_variables(ssa, loops)
    growth_traces = analyze.get_growth_traces(traces, key_variables)
    sequence = analyze.generate_sequence(growth_traces, key_variables, iterate_times)

    certificate = Certificate(args.gas_limit, sequence)
    print(certificate)


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
