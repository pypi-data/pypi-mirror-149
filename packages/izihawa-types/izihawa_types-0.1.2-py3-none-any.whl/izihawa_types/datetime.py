import numpy as np


class CustomDatetime:
    def __init__(self, dt: np.datetime64):
        self.dt = dt

    @staticmethod
    def from_timestamp(timestamp: int):
        return CustomDatetime(dt=np.datetime64(timestamp, 's'))

    @property
    def year(self) -> int:
        return self.dt.astype('datetime64[Y]').astype(int) + 1970

    @property
    def month(self) -> int:
        return self.dt.astype('datetime64[M]').astype(int) % 12 + 1

    @property
    def day(self) -> int:
        return self.dt - self.dt.astype('datetime64[M]') + 1
