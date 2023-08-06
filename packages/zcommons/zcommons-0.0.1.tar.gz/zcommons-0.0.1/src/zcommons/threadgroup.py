__all__ = [
    "ThreadGroup"
]

import threading

from .counter import MultiThreadCounter


class ThreadGroup(object):

    """
    Thread Group
    ============
    A simple thread group
    """

    def __init__(self):
        super(ThreadGroup, self).__init__()
        self.threads = []
        self.__counter = MultiThreadCounter()

    def __run(self, target, *args, **kwargs):
        self.__counter.inc()
        target(*args, **kwargs)
        self.__counter.dec()

    def add(self, target=None, name=None, args=(), kwargs=None, *, daemon=None) -> threading.Thread:
        """
        Add a thread, the meaning of the parameters is the same as ``threading.Thread`` class.

        :param target:
        :param name:
        :param args:
        :param kwargs:
        :param daemon:
        :return:
        """
        real_args = (target, *args)
        t = threading.Thread(target=self.__run, name=name, args=real_args, kwargs=kwargs, daemon=daemon)
        self.threads.append(t)
        return t

    def start(self) -> None:
        """
        Start all threads in group

        :return:
        """
        for t in self.threads:
            t.start()

    def join(self) -> None:
        """
        Wait until the thread group terminates.

        :return:
        """
        for t in self.threads:
            t.join()

    def done(self) -> bool:
        """
        Whether the all the threads are done.

        :return:
        """
        return self.__counter.count() == 0

    def alive_count(self) -> int:
        """
        The count of running threads.

        :return:
        """
        return self.__counter.count()

    def count(self) -> int:
        """
        The count of all threads.

        :return:
        """
        return len(self)

    def __len__(self):
        return len(self.threads)

    def __getitem__(self, item):
        return self.threads[item]
