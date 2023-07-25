class Accumulator:
    def __init__(self, limit: float) -> None:
        self.limit: float = limit
        self.value: float = 0.0

    def delay(self, delta_time: float) -> bool:
        self.value += delta_time
        if self.value >= self.limit:
            self.value = 0
            return True
        return False
