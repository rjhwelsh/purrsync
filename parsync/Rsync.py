#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import subprocess as sp
import os
import tempfile

import parsync.FileSet as FileSet


class Rsync:
    # Pathname constants
    MAIN = "main"
    PACKAGE = "pkg"
    ORPHAN = "orphan"
    ROOT = "root"
    BACKUP = "backup"

    def __init__(self,
                 source="/",
                 destination="./",
                 mainSet=FileSet.FileSet(),
                 ignoreSet=FileSet.FileSet(),
                 packageSet=dict(),
                 rsyncBin="",
                 rsyncArgs=list()):
        """
        This class provides an interface to rsync w/ filesets.
        """
        self.source = source
        self.destination = destination
        self.mainSet = mainSet
        self.ignoreSet = ignoreSet
        self.packageSet = packageSet
        self.rsyncArgs = rsyncArgs
        self.rsyncBin = rsyncBin

        # Override
        if not rsyncBin:
            self.rsyncBin = self.which()

    def which(self):
        """ Returns which rsync is being used by the system. """
        with sp.Popen(["which", "rsync"],
                      stdout=sp.PIPE) as proc:
            return proc.stdout.read().decode(
                "utf-8").rstrip(os.linesep)

    def rsync(self,
              filelist,
              src,
              dest
              ):
        """ Uses rsync to synchronize files based on filelists. """
        filesfrom = "--files-from=" + filelist
        with sp.Popen([self.rsyncBin,
                       self.rsyncArgs,
                       filesfrom,
                       src,
                       dest],
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

            src = self.source
            dest = os.path.join(self.destination,
                                self.MAIN,
                                self.ROOT)

            syncFileSet.write()
            return self.rsync(syncCacheFile.name,
                              src,
                              dest)
