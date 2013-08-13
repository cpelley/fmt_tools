"""
Timer class for simple benchmarking

"""
# Copyright (c) 2013 Carwyn Pelley
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
