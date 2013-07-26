#!/usr/bin/env python

"""remove whitespace/emptylines from specified filetypes"""
import collections
import argparse
import os
import re
import difflib


__author__ = "Carwyn Pelley"
__copyright__ = "2013, Carwyn Pelley"
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


def tree_find(dname, ext_filter, recursive=True):
    # Return all files recursively under specified directory that match filter
    flist = []
    if recursive is not True:
        root, dirs, fnames = next(os.walk(dname))
        for fname in fnames:
            if os.path.splitext(fname)[1] in ext_filter:
                flist.append(os.path.join(root, fname))
    else:
        for root, dirs, fnames in os.walk(dname):
            for fname in fnames:
                if os.path.splitext(fname)[1] in ext_filter:
                    flist.append(os.path.join(root, fname))
    return flist


def update_file(fname, nlines):
    # Overwrite the file with whitespace removed
    with open(fname, 'w') as f:
        f.writelines(nlines)


if __name__ == '__main__':
    prog_desc = """
    This program allows whitespace removal at a specified location over a
    specified list of filetypes.  Filetype matching can also occur recursively
    if chosen and additionally a debug mode can be chosen which invokes a diff
    preview of the changes to be made as apposed to making actual changes.

    Default setting's are a non-recursive whitespace removal of python
    specific filetypes (.py and .pyx).
    """
    parser = argparse.ArgumentParser(prog='Whitespace remover',
                                     description=prog_desc)
    parser.add_argument('--location', '-l', default=os.getcwd(), type=str,
                        help=('Location to apply whitespace removal '
                              '(default: ./)'))

    parser.add_argument('--filter', '-f', default=LAN_FMT['python'],
                        nargs='+', type=str,
                        help=('Filter filetypes, '
                              '(default: {})'.format(LAN_FMT['python'])))

    parser.add_argument('--recursive', '-r', action='store_true',
                        help=('Turn on/off recursive matching, '
                              '(default: True)'))

    parser.add_argument('--debug', '-d', action='store_true',
                        help=('Debug mode does a print out of the files that '
                              'would change (default: False)'))
    parser.add_argument('--diff', '-df', action='store_true',
                        help=('Implements a diff of the changes '
                              'that will be made without actually making '
                              'them (default: False)'))

    args = parser.parse_args()

    if args.debug:
        print '\nchosen arguments: {}'.format(args)

    flist = tree_find(args.location, args.filter, args.recursive)

    updated = collections.Counter()
    for fname in flist:
        nlines, diff = rm_whitespace(fname)
        for dd in diff:
            if nlines:
                updated.update([fname])
                if args.diff is True:
                    print dd
                if args.debug is not True:
                    update_file(fname, nlines)
                    break

    if args.debug is True:
        msg = 'file change preview: {}, {} lines difference'
    else:
        msg = 'updating: {}, {} lines changed'
    for fname in updated.iteritems():
        print msg.format(*fname)
    print '\ncompleted'
