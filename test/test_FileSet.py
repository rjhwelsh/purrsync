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

    def test_FileClobber(self):
        with tempfile.NamedTemporaryFile(mode='r',
                                         newline=os.linesep) as fp:
            with open(fp.name, 'w') as fpw:
                fpw.write('manually_added_file.txt')

            fs1 = FileSet.FileSet(filename=fp.name)
            fs1.add('somefile.txt')

            self.assertEqual(
                fs1.read(),
                set({
                    'manually_added_file.txt',
                    'somefile.txt'}))

    def test_fnupdate(self):
        def fibonacci(n):
            """ A generator for fibonacci numbers. """
            a, b, counter = 0, 1, 0
            while True:
                if (counter > n):
                    return
                yield a
                a, b = b, a + b
                counter += 1

        def fibonacciString(n):
            """ A generator for fibonacci strings. """
            for f in fibonacci(n):
                yield(str(f))

        fs1 = FileSet.FileSet(updatefn=fibonacci(5))
        with self.assertRaises(TypeError):
            fs1.fnupdate()
            fs1.read()

        fs1.updatefn = fibonacciString(5)
        fs1.fnupdate()
        self.assertEqual(fs1.read(),
                         set({'0', '1', '2', '3', '5'}))

    def test_root(self):
        fs1 = FileSet.FileSet(root='/')
        fs1.add('./somefile.txt')
        fs1.add('somefile.txt')
        fs1.add('/somefile.txt')
        self.assertEqual(len(fs1.read()), 1)


if __name__ == '__main__':
    unittest.main()
