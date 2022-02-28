"""
Timer class for simple benchmarking

"""
# Copyright (c) 2022 Carwyn Pelley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from contextlib import contextmanager
from time import time


class TimeIt:
    def __init__(self, verbose=False):
        self._verbose = verbose
        self._elapsed = None
        self._start = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self._elapsed = time.perf_counter() - self._start
        if self.verbose:
            print(str(self))

    @property
    def elapsed(self):
        """Return elapsed time in seconds."""
        return self._elapsed

    def __str__(self):
        """Print elapsed time in seconds."""
        return f"Run-time: {self._elapsed}s"


@contextmanager
def timeit(t1=None):
    """
    Timming a code snippet.

    Function returns the number of seconds between the specified time or
    entering the context manager and exiting the context manager.

    Kwargs:

    * t1 (time.time):
        Start time in seconds since epoch, in UTC.

    For example::

        with timeit():
            some_hungry_operation()

    """
    if t1 is None:
        t1 = time.perf_counter()
    yield
    print time.perf_counter() - t1
