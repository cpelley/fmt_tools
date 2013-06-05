"""Timer class for simple benchmarking"""

import datetime
import inspect


class TimeIt(object):
    def __init__(self, t1=None):
        """
        Timming a code snippet.

        Kwargs:

        * t1 (datetime object):
            Start time

        .. note::

            A timedelta object is assigned to self.result and trace
            information storred in self.location

        """
        if t1:
            self.t1 = t1
        else:
            self.t1 = None
        self.t2 = None

        frame, fnme, lineno, func_nme, lines, _ = inspect.getouterframes(
            inspect.currentframe())[1]
        self.location = '> {}({}){}\n->{}'.format(
            fnme, lineno, func_nme, lines[0])

    def __enter__(self):
        self.t1 = datetime.datetime.now()
        return self

    def __exit__(self, type, value, traceback):
        self.t2 = datetime.datetime.now()
        self.result = self.t2 - self.t1
        self.scr_print()

    def scr_print(self):
        print self.location
        print 'completed in {}\n'.format(self.t2 - self.t1)