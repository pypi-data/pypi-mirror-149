__all__ = [
    "Counter",
    "LockFreeCounter",
    "MultiThreadCounter",
    "MultiProcessCounter"
]

import itertools
import threading
import multiprocessing


class Counter(object):
    """
    Basic Counter
    =============
    The basic and fastest counter, non-thread-safe, only can be used in single thread.
    """

    def __init__(self, v: int = 0, step: int = 1):
        super(Counter, self).__init__()
        self._v = v
        self._step = step

    def inc(self) -> None:
        """
        let ``count`` increase ``step``

        :return:
        """
        self._v += self._step

    def dec(self) -> None:
        """
        let ``count`` decrease ``step``

        :return:
        """
        self._v -= self._step

    def count(self) -> int:
        """
        the current value of counter

        :return: an int value.
        """
        return self._v


class LockFreeCounter(Counter):

    """
    Lock-Free Counter
    =================
    The thread-safe counter in CPython.
    Due to the GIL, CPython can implement lock-free counter
    """

    def __init__(self, v: int = 0, step: int = 1):
        super(LockFreeCounter, self).__init__(v, step)
        self._r_cnt = itertools.count(v, step)
        self._l_cnt = itertools.count(0, step)

    def inc(self) -> None:
        next(self._r_cnt)

    def dec(self) -> None:
        next(self._l_cnt)

    def count(self) -> int:
        return next(self._r_cnt) - next(self._l_cnt)


class MultiThreadCounter(Counter):

    """
    Multi-Thread Counter
    ====================
    The thread-safe counter for every python interpreter.
    Due to this implementation uses lock, it is slower than ``LockFreeCounter``.
    """

    def __init__(self, v: int = 0, step: int = 1):
        super(MultiThreadCounter, self).__init__(v, step)
        self._lock = threading.Lock()

    def inc(self) -> None:
        with self._lock:
            self._v += self._step

    def dec(self) -> None:
        with self._lock:
            self._v -= self._step

    def count(self) -> int:
        return self._v


class MultiProcessCounter(Counter):

    """
    Multi-Process Counter
    =====================
    The process-safe counter.
    Due to process sync, this counter is the slowest counter.
    """

    def __init__(self, v: int = 0, step: int = 1):
        super(MultiProcessCounter, self).__init__(v, step)
        self._v = multiprocessing.Value("l", v)
        self._step = multiprocessing.Value("l", step)

    def inc(self) -> None:
        with self._v.get_lock():
            self._v.value = self._v.value + self._step.value

    def dec(self) -> None:
        with self._v.get_lock():
            self._v.value = self._v.value - self._step.value

    def count(self) -> int:
        return self._v.value
