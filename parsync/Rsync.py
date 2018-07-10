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
                 rsyncArgs=""):
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

        with sp.Popen([self.rsyncBin] +
                      self.rsyncArgs.split() +
                      [filesfrom,
                       src,
                       dest],
                      stdout=sp.PIPE) as proc:
            return proc.stdout.read().decode(
                "utf-8").rstrip(os.linesep)

    def rsyncMain(self):
        """ Rsyncs main set. """
        with tempfile.NamedTemporaryFile(mode='r') as syncCacheFile:
            syncSet = self.mainSet - self.ignoreSet
            syncSet.filename = syncCacheFile.name
            syncSet.write()

            src = self.source
            dest = os.path.join(self.destination,
                                self.MAIN,
                                self.ROOT)

            return self.rsync(syncCacheFile.name,
                              src,
                              dest)

    def rsyncPackages(self):
        """ Rsyncs packages. """
        mainSet = self.mainSet - self.ignoreSet
        for name, pSet in self.packageSet.items():
            with tempfile.NamedTemporaryFile(mode='r') as syncCacheFile:
                syncSet = mainSet & pSet
                syncSet.filename = syncCacheFile.name
                syncSet.write()

                src = self.source
                dest = os.path.join(self.destination,
                                    self.PACKAGE,
                                    name,
                                    self.ROOT)

                yield (name, self.rsync(
                    syncCacheFile.name,
                    src,
                    dest))

    def rsyncOrphans(self):
        """ Rsyncs orphaned files. """
        mainSet = self.mainSet - self.ignoreSet
        orphanSet = self.mainSet - self.ignoreSet
        for pSet in self.packageSet.values():
            orphanSet = orphanSet - (mainSet & pSet)

        with tempfile.NamedTemporaryFile(mode='r') as syncCacheFile:
            orphanSet.filename = syncCacheFile.name
            orphanSet.write()
            src = self.source
            dest = os.path.join(self.destination,
                                self.ORPHAN,
                                self.ROOT)
            return self.rsync(syncCacheFile.name,
                              src,
                              dest)

    def prepareDest(self, main=True, package=True, orphan=True):
        """ Prepares destination directory for rsync. """
        # NB. This probably won't work on Windows Systems.
        if self.__isSshDest():
            return self.__prepareSshDest(main, package, orphan)
        else:
            return self.__prepareLocalDest(main, package, orphan)

    def __isSshDest(self):
        root = self.destination.split(os.sep)[0]
        if root:
            return root[-1] == ":"
        else:
            return False

    def __prepareLocalDest(self,
                           main,
                           package,
                           orphan):
        DEST = self.destination
        DEST_MAIN = os.path.join(DEST, self.MAIN)
        DEST_MAIN_ROOT = os.path.join(DEST_MAIN, self.ROOT)
        DEST_ORPHAN = os.path.join(DEST, self.ORPHAN)
        DEST_ORPHAN_ROOT = os.path.join(DEST_ORPHAN, self.ROOT)
        DEST_PACKAGE = os.path.join(DEST, self.PACKAGE)
        if not os.path.isdir(DEST):
            raise ValueError("DEST must exist and be a directory!")

        if main:
            if not os.path.isdir(DEST_MAIN):
                os.mkdir(DEST_MAIN)
            if not os.path.isdir(DEST_MAIN_ROOT):
                os.mkdir(DEST_MAIN_ROOT)

        if orphan:
            if not os.path.isdir(DEST_ORPHAN):
                os.mkdir(DEST_ORPHAN)
            if not os.path.isdir(DEST_ORPHAN_ROOT):
                os.mkdir(DEST_ORPHAN_ROOT)

        if package:
            if not os.path.isdir(DEST_PACKAGE):
                os.mkdir(DEST_PACKAGE)
            for DEST_PACKAGE_I in self.packageSet.keys():
                DEST_PACKAGE_ROOT = os.path.join(
                    DEST_PACKAGE,
                    DEST_PACKAGE_I,
                    self.ROOT)
                if not os.path.isdir(DEST_PACKAGE_ROOT):
                    os.makedirs(DEST_PACKAGE_ROOT)
        return 0

    def __prepareSshDest(self,
                         main,
                         package,
                         orphan):
        raise NotImplementedError
