#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import subprocess as sp
import os
import tempfile

import parsync.FileSet as FileSet


class Rsync:
    def __init__(self,
                 mainSet=FileSet.FileSet(),
                 ignoreSet=FileSet.FileSet(),
                 packageSet=dict(),
                 rsyncBin="",
                 rsyncArgs=""):
        """
        This class provides an interface to rsync w/ filesets.
        """
        self.mainSet = mainSet
        self.ignoreSet = ignoreSet
        self.packageSet = packageSet
        self.rsyncArgs = rsyncArgs
        self.rsyncBin = rsyncBin

    def which(self):
        """ Returns which rsync is being used by the system. """
        with sp.Popen(["which", "rsync"],
                      stdout=sp.PIPE) as proc:
            return proc.stdout.read().decode(
                "utf-8").rstrip(os.linesep)
    def rsyncMain(self):
        """ Rsyncs main set. """
        with tempfile.NamedTemporaryFile(mode='r') as syncCacheFile:

            mainSet = self.mainSet.read()
            ignoreSet = self.ignoreSet.read()
            syncSet = mainSet - ignoreSet

            syncFileSet = FileSet.FileSet(
                setIter=syncSet,
                filename=syncCacheFile.name)

            syncFileSet.write()
            return self.rsync(syncCacheFile.name)
