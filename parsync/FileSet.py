#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import os


class FileSet(set):
    def __init__(self, setIter=set(), filename=None, updatefn=None, root=None):
        """ Initialize FileSet
        Args:
            filename (str): Filename to read/write to.
            updatefn (method): Command to update filelist.
            root (str): Root prefix for relative paths.

        """

        self.clear()
        self.update(setIter)

        self.filename = filename
        self.updatefn = updatefn
        self.root = root

    def read(self):
        """
        Reads file into set.
        """
        if not isinstance(self.filename, type(None)):
            with open(self.filename, 'r') as f:
                lines = f.read().splitlines()
                lineset = set(lines)
            self.update(lineset)
        return self.normpath()

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
        for i in self.updatefn:
            if not isinstance(i, str):
                raise TypeError(
                    'Output of self.updatefn must be a string! ' +
                    'Received {} instead!'.format(type(i)))
            self.add(i)
        return set(self)

    def normpath(self):
        """ Returns the set with normalized paths."""
        return set({self.__path(item)
                    for item in self})

    def __path(self, pathstring):
        """
        Returns the filepath joined with root (prefix)
        If root is None, the pathstring is unmodified.
        """
        if isinstance(self.root, type(None)):
            return pathstring
        return os.path.normpath(
            os.path.join(
                self.root, pathstring))

    def __relpath(self, pathstring):
        """
        Returns a pathstring after removing root.
        If root is not present, an error will be raised.
        If root is None, the pathstring is unmodified.
        """
        if isinstance(self.root, type(None)):
            return pathstring

        norm_root = os.path.normpath(self.root)
        norm_path = os.path.normpath(pathstring)

        norm_path_stripped = norm_path.lstrip(norm_root)

        if (norm_path_stripped < norm_path
                or norm_root == os.sep):
            return norm_path_stripped
        else:
            raise ValueError('Could not lstrip "{}" from "{}"'.format(
                norm_root, norm_path))

    # Override Methods
    def union(self, *others):
        newSet = self.copy()
        for s in others:
            newSet.update(
                set({self.__relpath(i)
                     for i in s.normpath()}))
        return newSet

    def intersection(self, *others):
        newSet = self.copy()
        for s in others:
            newSet.intersection_update(
                set({self.__relpath(i)
                     for i in s.normpath()}))
        return newSet

    def difference(self, *others):
        newSet = self.copy()
        for s in others:
            newSet.difference_update(
                set({self.__relpath(i)
                     for i in s.normpath()}))
        return newSet

    def copy(self):
        """ Returns a copy of FileSet. """
        return FileSet(setIter=set(self),
                       filename=None,
                       updatefn=self.updatefn,
                       root=self.root)

    def __eq__(self, other):
        if (self.root == other.root and
                self.updatefn == other.updatefn and
                set(self) == set(other)):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __set__(self):
        """ Returns a plain set of FileSet. """
        return set({item for item in self})

    def __or__(self, other):
        return self.union(other)

    def __and__(self, other):
        return self.intersection(other)

    def __sub__(self, other):
        return self.difference(other)


