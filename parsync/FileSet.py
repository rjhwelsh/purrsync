#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import os


class FileSet(set):
    def __init__(self, filename=None, updatefn=None, root=None):
        """ Initialize FileSet
        Args:
            filename (str): Filename to read/write to.
            updatefn (method): Command to update filelist.
            root (str): Root prefix for relative paths.

        """
        self.filename = filename
        self.updatefn = updatefn
        self.root = root

    def read(self):
        """
        Reads file into set.
        """
        with open(self.filename, 'r') as f:
            lines = f.read().splitlines()
        lineset = set(lines)
        self.clear()
        self.update(lineset)
        return set(self)

    def write(self):
        """
        Writes FileSet to filename.
        """
        strings = list(self)
        strings.sort()
        with open(self.filename, 'w') as f:
            f.write(os.linesep.join(strings))

    def fnupdate(self):
        """
        Executes the updatefn function to update the list.
        """
        for i in self.updatefn():
            self.add(i)
        return set(self)
