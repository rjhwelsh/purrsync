#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import unittest
import tempfile
import os
import parsync.FileSet as FileSet


class TestFileSet(unittest.TestCase):

    def test_Init(self):
        fs1 = FileSet.FileSet()
        self.assertEqual(fs1.filename, None)
        self.assertEqual(fs1.updatefn, None)
        self.assertEqual(fs1.root, None)

    def test_SetBasic(self):
        fs1 = FileSet.FileSet()
        fs1.add('somefile.txt')
        fs1.add('somefile.txt')
        self.assertEqual(len(fs1), 1)

    def test_FileOps(self):
        with tempfile.NamedTemporaryFile(mode='r',
                                         newline=os.linesep) as fp:
            fs1 = FileSet.FileSet(filename=fp.name)
            self.assertFalse(fs1.read())
            fs1.add('somefile.txt')
            fs1.write()
            self.assertTrue(fs1.read())
            fs1.add('anotherfile.txt')
            fs1.write()
            expectedString = fp.read()
            self.assertEqual(expectedString, 'anotherfile.txt\nsomefile.txt')



if __name__ == '__main__':
    unittest.main()
