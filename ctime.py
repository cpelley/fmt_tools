import datetime
import inspect


class TimeIt(object):
    def __init__(self, t1=None):
        """Timming a code snipper."""
        if t1:
            self.t1 = t1
        else:
            self.t1 = None
        self.t2 = None

        self.line1 = inspect.stack()[1]

    def __enter__(self):
        self.t1 = datetime.datetime.now()
        return self

    def __exit__(self, type, value, traceback):
        self.t2 = datetime.datetime.now()
        print 'completed in {}'.format(self.t2 - self.t1)
