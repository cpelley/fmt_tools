#! /usr/bin/python

import os
from glob import glob
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
