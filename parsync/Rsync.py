#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>


class Rsync:
    def __init__(self, mainSet, ignoreSet, packageSet, rsyncArgs):
        """
        This class provides an interface to rsync w/ filesets.
        """
        self.mainSet = mainSet
        self.ignoreSet = ignoreSet
        self.packageSet = packageSet
        self.rsyncArgs = rsyncArgs
