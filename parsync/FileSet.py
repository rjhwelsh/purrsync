#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import os


class FileSet(set):
    def __init__(self, filename=None, cmd=None, root=None):
        """ Initialize FileSet
        Args:
            filename (str): Filename to read/write to.
            cmd (method): Command to update filelist.
            root (str): Root prefix for relative paths.

        """
        self.filename = filename
        self.cmd = cmd
        self.root = root

    def read(self):
        with open(self.filename, 'r') as f:
            lines = f.read().splitlines()
        lineset = set(lines)
        self.clear()
        self.update(lineset)
        return set(self)

    def write(self):
        strings = list(self)
        strings.sort()
        with open(self.filename, 'w') as f:
            f.write(os.linesep.join(strings))
