import argparse
import logging

from src.rattle import Recover
from src.sym_exec.symbolic_executor import SymExec

logger = logging.getLogger()


def main():
    default_max_depth = 25
    default_timeout = 100

    parser = argparse.ArgumentParser(description='demo')
    parser.add_argument(
        '--input', '-i', type=argparse.FileType('rb'), help='input evm file')
    parser.add_argument('--max-depth', '-md', type=int, default=default_max_depth,
                        help=f'Max recursion depth. The counting is how many basic blocks should be analysed. Default = {default_max_depth}')
    parser.add_argument('--timeout', '-t', type=int, default=default_timeout,
                        help=f'Timeout to Z3 Solver. Default = {default_timeout}')
    args = parser.parse_args()
    filename = args.input.name
    logger.info(f'Analyzing file: {filename}')
    bytecode = args.input.read()

    try:
        ssa = Recover(bytecode, edges=[], optimize=True)

        traces = SymExec(ssa, args.max_depth).execute()
        print("Found", len(traces), "traces")

    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
