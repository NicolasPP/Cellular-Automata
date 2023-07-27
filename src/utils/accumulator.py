class Accumulator:
    def __init__(self, limit: float) -> None:
        self.limit: float = limit
        self.value: float = 0.0
        self.total_elapsed_time: float = 0
        self.total_frames: int = 0

    def delay(self, delta_time: float) -> bool:
        self.total_frames += 1
        self.total_elapsed_time += delta_time
        self.value += delta_time
        if self.value >= self.limit:
            self.value = 0
            return True
        return False

    def set_limit(self, limit: float) -> None:
        if limit <= 0: return
        average_frame_time: float = self.get_average_frame_duration()
        if limit < average_frame_time and self.limit > limit:
            return
        print(self.get_average_frame_duration())
        print(self.limit, "--> limit")
        self.limit = limit

    def get_limit(self) -> float:
        return self.limit

    def get_average_frame_duration(self) -> float:
        if self.total_frames == 0: return 0
        return self.total_elapsed_time / self.total_frames

    def reset(self) -> None:
        self.total_frames = 0
        self.total_elapsed_time = 0
