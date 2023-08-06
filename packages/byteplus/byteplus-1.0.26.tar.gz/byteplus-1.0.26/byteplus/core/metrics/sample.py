import threading
import numpy as np


def sample_max(values: list) -> float:
    if len(values) == 0:
        return 0.0
    return max(values)


def sample_min(values: list) -> float:
    if len(values) == 0:
        return 0.0
    return min(values)


def sample_mean(values: list) -> float:
    if len(values) == 0:
        return 0.0
    return np.mean(values)


def sample_percentile(values: list, p: float) -> float:
    if len(values) == 0:
        return 0.0
    return np.percentile(values, p)


class Sample(object):
    def __init__(self, reservoir_size: int):
        self.count:int = 0
        self.lock = threading.Lock()
        self.reservoir_size: int = reservoir_size
        self.values:list = []

    def clear(self):
        with self.lock:
            self.count = 0
            self.values.clear()

    # returns the number of samples recorded, which may exceed the
    # reservoir size.
    def count(self):
        with self.lock:
            return self.count

    def max(self):
        with self.lock:
            return sample_max(self.values)

    def avg(self):
        with self.lock:
            return sample_mean(self.values)

    def min(self):
        with self.lock:
            return sample_min(self.values)

    def percentile(self, p: float):
        with self.lock:
            return sample_percentile(self.values, p)

    # returns the size of the sample, which is at most the reservoir size.
    def size(self):
        with self.lock:
            return len(self.values)

    def snapshot(self):
        with self.lock:
            return SampleSnapshot(self.count, np.copy(self.values))

    # amples a new value.
    def update(self, v):
        with self.lock:
            self.count = self.count + 1
            if len(self.values) < self.reservoir_size:
                self.values.append(v)
            else:
                r = np.random.randint(self.count)
                if r < len(self.values):
                    self.values[r] = v


class SampleSnapshot(object):
    def __init__(self, count: int, values: list):
        self.count = count
        self.values = values

    def count(self):
        return self.count

    def max(self):
        return sample_max(self.values)

    def avg(self):
        return sample_mean(self.values)

    def min(self):
        return sample_min(self.values)

    def percentile(self, p: float):
        return sample_percentile(self.values, p)

    def size(self):
        return len(self.values)

    def pct75(self):
        return sample_percentile(self.values, 0.75)

    def pct90(self):
        return sample_percentile(self.values, 0.90)

    def pct95(self):
        return sample_percentile(self.values, 0.95)

    def pct99(self):
        return sample_percentile(self.values, 0.99)

    def pct999(self):
        return sample_percentile(self.values, 0.999)

    def get_func_from_name(self, func_name: str):
        return getattr(self, func_name)
