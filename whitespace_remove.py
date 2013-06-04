#!/usr/bin/env python

"""remove whitespace/emptylines from specified filetypes"""

import os
import re
import difflib


__author__ = "Carwyn Pelley"
__license__ = "LGPLv3"
__version__ = "0.9.0"
__email__ = "cpelley.pub@gmail.com"


LAN_FMT = {'python': ['.py', '.pyx']}


def rm_whitespace(fname):
    # Load file, remove whitespace and return result with corresponding diff
    with open(fname, 'r') as f:
        lines = f.readlines()

    # Remove whitespace
    nlines = []
    for ind, line in enumerate(lines):
        if ind == len(lines) - 1:
            nlines.append(re.sub('[\t ]*$', '', line))
        else:
            nlines.append(re.sub('[\t ]*$\n', '\n', line))

    # Remove empty lines
    ind = None
    for ind, line in enumerate(nlines[::-1]):
        if line != '\n':
            break
    if ind:
        nlines = nlines[:-(ind)]
        # Replace with '\n' to ensure newline at file end (pep8)
        nlines[-1] = re.sub('[\t ]*$\n', '\n', nlines[-1])

    # Create diff of the result
    diff = difflib.unified_diff(lines, nlines, fromfile=fname, tofile=fname)

    return nlines, diff


def tree_find(dname=os.getcwd(), ext_filter=LAN_FMT['python']):
    # Return all files recursively under specified directory that match filter
    flist = []
    for root, _, fnames in os.walk(dname):
        for fname in fnames:
            if os.path.splitext(fname)[1] in ext_filter:
                flist.append(os.path.join(root, fname))
    return flist


def update_file(fname, nlines):
    # Overwrite the file with whitespace removed
    with open(fname, 'w') as f:
        f.writelines(nlines)


if __name__ == '__main__':
    flist = tree_find()
    debug = False

    for fname in flist:
        nlines, diff = rm_whitespace(fname)
        if debug:
            for dd in diff:
                print dd
        elif nlines:
            # Test is generator is empty
            try:
                diff.next()
                print 'updating: {}'.format(fname)
                update_file(fname, nlines)
            except StopIteration:
                pass
    print 'completed'
