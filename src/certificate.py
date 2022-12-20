class Certificate(object):
    def __init__(self, gas_limit = 30_000_000):
        self.gas_limit = gas_limit
        self.squence = None
        self.is_vulnerable = False

    def __str__(self) -> str:
        pass