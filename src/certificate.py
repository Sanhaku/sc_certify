from src.loop import Loop


class Certificate(object):
    def __init__(self, gas_limit=30_000_000, loops: list(Loop) = []):
        self.gas_limit = gas_limit
        self.loops = []

    def __str__(self) -> str:
        # TODO: format certificate string for printing
        pass
