#!/usr/bin/env python
"""
wrapper for compiling latex documents

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

from glob import glob
import os
import sys


class CompileLatex():
    def __init__(self, cmdseq, name='main'):
        self.command = dict({
            'delete': None,
            'makeindex': ('makeindex {name}.nlo -s nomencl.ist '
                          '-o {name}.nls'.format(name)),
            'bibtex': 'bibtex {}'.format(name),
            'latex': 'latex {}'.format(name),
            'mkps': 'dvips {name}.dvi -o {name}.ps'.format(name),
            'mkpdf': 'ps2pdf {}.ps'.format(name)})
        self.cmdseq = cmdseq

    def deletetmpfile(self):
        filedel = ['*.aux', '*.log', '*.ps', '*.dvi', '*.toc',
                   '*.lof', '*.nls', '*.lot', '*.bbl', '*.blg',
                   '*.txt', '*.bak', '*.nlo', '*.ilg', '*.dvi', '*.out']
        for fdel in filedel:
            tmp = glob(fdel)
            if len(tmp) > 0:
                for f in tmp:
                    os.remove(f)

    def compile(self):
        for cmd in self.cmdseq:
            if cmd == 'delete':
                print 'deleting temp files'
                self.deletetmpfile()
            else:
                print 'command: %s' % (cmd)
                retval = os.system(self.command[cmd])
                print self.command[cmd]
                if retval != 0:
                    sys.exit()
                print 'completed'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        name = sys.argv[1]

    print 'compilation: started'
    cmdseq = ['delete', 'latex', 'latex', 'bibtex', 'makeindex',
              'latex', 'latex', 'mkps', 'mkpdf', 'delete']
    lc = CompileLatex(cmdseq, name=name)
    lc.compile()
    print '##########################################'
    print 'compilation: completed'
