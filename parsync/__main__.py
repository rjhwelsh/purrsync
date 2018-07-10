#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import argparse
import subprocess as sp



def main():
    parser = argparse.ArgumentParser(
        description='A wrapper for rsync.')
    parser.add_argument(
        'source',
        metavar='SRC',
        type=str,
        nargs='?',
        # required=True,
        help='Source for rsync')
    parser.add_argument(
        'destination',
        metavar='DEST',
        type=str,
        nargs='?',
        # required=True,
        help='Destination for rsync')
    parser.add_argument(
        '-m', '--main-file',
        metavar='MAIN_FILE',
        type=str,
        nargs='?',
        help='Main list of files to sync')
    parser.add_argument(
        '-i', '--ignore-file',
        metavar='IGNORE_FILE',
        type=str,
        nargs='?',
        help='Ignore list of files')
    parser.add_argument(
        '-p', '--package',
        action='store_true',
        help='Create a directory in DEST for packaged files.')
    parser.add_argument(
        '-o', '--orphans',
        action='store_true',
        help='Create a directory in DEST for orphaned files.\n' +
        '(files without packages)')
    parser.add_argument(
        '-D', '--package-dir',
        metavar='PKG_DIR',
        type=str,
        nargs='?',
        help='Package directory of package file lists.')
    parser.add_argument(
        '-x', '--main-exec',
        metavar='MAIN_EXEC',
        type=str,
        nargs='?',
        help='Use MAIN_EXEC to produce a file list.')
    parser.add_argument(
        '-y', '--ignore-exec',
        metavar='IGNORE_EXEC',
        type=str,
        nargs='?',
        help='Use IGNORE_EXEC to produce an ignore list.')
    parser.add_argument(
        '-e', '--package-exec',
        metavar='PKG_EXEC',
        type=str,
        nargs='?',
        help='Use PKG_EXEC to produce a file list for each package,\n' +
        '{} is replaced with the package name.')
    parser.add_argument(
        '-L', '--package-list-exec',
        metavar="PKG_LIST_EXEC",
        type=str,
        nargs='?',
        help='Use PKG_LIST_EXEC to produce a list of packages.')
    parser.add_argument(
        '-r', '--alt-root',
        metavar='ALT_ROOT',
        type=str,
        nargs='?',
        help='Use alternative root, instead of SRC for filelists.')
    parser.add_argument(
        '-A', '--rsync-args',
        metavar='RSYNC_ARGS',
        type=str,
        nargs='?',
        help='Use these arguments with rsync.')
    parser.add_argument(
        '-B', '--rsync-bin',
        metavar='RSYNC_BIN',
        type=str,
        nargs='?',
        help='Specify an alternative path to rsync binary.')

    # parser.parse_args()


def updateIter(execstring):
    """ Generates an iterable for shell execstring. """
    proc = sp.Popen(execstring,
                    shell=True,
                    stdout=sp.PIPE)
    for item in proc.stdout.read(
    ).decode(
        "utf-8").rstrip(
            os.linesep).split(
                os.linesep):
        yield item


if __name__ == '__main__':
    main()
