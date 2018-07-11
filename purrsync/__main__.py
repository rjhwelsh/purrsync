#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import sys
import os
import argparse
import subprocess as sp

from purrsync import FileSet
from purrsync import Rsync


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
        '-o', '--orphan',
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
        default=str(),
        help='Use these arguments with rsync.')
    parser.add_argument(
        '-B', '--rsync-bin',
        metavar='RSYNC_BIN',
        type=str,
        nargs='?',
        default=str(),
        help='Specify an alternative path to rsync binary.')

    args = parser.parse_args()

    main_update = []
    if args.main_exec:
        main_update = updateIter(
            args.main_exec)

    ignore_update = []
    if args.ignore_exec:
        ignore_update = updateIter(
            args.ignore_exec)

    package_list_update = []
    if args.package_list_exec:
        package_list_update = updateIter(
            args.package_list_exec)

    pkgfn = None
    if args.package_exec:
        def pkgfn(package):
            return updateIter(
                args.package_exec.format(
                    package))

    root = args.source
    if args.alt_root:
        root = args.alt_root

    mainSet = FileSet.FileSet(
        setIter=input_pipe(),
        filename=args.main_file,
        updatefn=main_update,
        root=root)
    mainSet.read()
    mainSet.fnupdate()

    ignoreSet = FileSet.FileSet(
        filename=args.ignore_file,
        updatefn=ignore_update,
        root=root)
    ignoreSet.read()
    ignoreSet.fnupdate()

    packageSet = dict()
    if args.package:
        packageSet = FileSet.PackageSource(
            pkglist=package_list_update,
            dirname=args.package_dir,
            pkgfn=pkgfn,
            root=root)
        packageSet.read()
        packageSet.fnupdate()

    rsyncInstance = Rsync.Rsync(source=args.source,
                                destination=args.destination,
                                mainSet=mainSet,
                                ignoreSet=ignoreSet,
                                packageSet=packageSet,
                                rsyncBin=args.rsync_bin,
                                rsyncArgs=args.rsync_args)
    rsyncInstance.prepareDest(package=args.package,
                              orphan=args.orphan)
    rsyncInstance.rsyncMain()

    if args.package:
        for pkg, proc in rsyncInstance.rsyncPackages():
            pass

    if args.orphan:
        rsyncInstance.rsyncOrphans()


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


def input_pipe():
    if not sys.stdin.isatty():
        input_stream = sys.stdin
        for line in input_stream:
            yield(
                line.rstrip(
                    os.linesep))


if __name__ == '__main__':
    main()
