#!/usr/bin/env python

"""remove whitespace/emptylines from specified filetypes"""

import os
import re
import difflib


__author__ = "Carwyn Pelley"
__license__ = "LGPLv3"
__version__ = "0.5.0"
__email__ = "cpelley.pub@gmail.com"


LAN_FMT = {'python':['.py', '.pyx']}


def rm_whitespace(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    nlines = []
    for ind, line in enumerate(lines):
        if ind == len(lines)-1:
            nlines.append(re.sub('[\t ]*$', '', line))
        else:
            nlines.append(re.sub('[\t ]*$\n', '\n', line))

    # Remove empty lines
    for ind, line in enumerate(nlines[::-1]):
        if line:
            break
    if ind:
        nlines = nlines[:-(ind)]

    diff = difflib.unified_diff(lines, nlines, fromfile=fname, tofile=fname)

    return lines, diff


def tree_find(dname=os.getcwd(), ext_filter=LAN_FMT['python']):
    flist = []
    for root, _, fnames in os.walk(dname):
        for fname in fnames:
            if os.path.splitext(fname)[1] in ext_filter:
                flist.append(os.path.join(root, fname))
    return flist


def update_file(fname, nlines):
    with open(fname, 'w') as f:
        f.write(nlines)


if __name__ == '__main__':
    flist = tree_find('/home/carwyn/git/fmt_tools')
    debug = True

    for fname in flist:
        nlines, diff = rm_whitespace(fname)
        if debug:
            for dd in diff:
                print dd
        else:
            update_file(fname, nlines)
        
        



