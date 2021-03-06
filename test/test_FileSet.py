#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import unittest
import tempfile
import os
import subprocess as sp
import purrsync.FileSet as FileSet


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

    def test_SetOperators(self):
        set1 = set({'somefile.txt',
                    'anotherfile.txt'})
        set2 = set({'somefile.txt'})
        set3 = set1 - set2

        fs1 = FileSet.FileSet(setIter=set1, root='/')
        fs2 = FileSet.FileSet(setIter=set2, root='/')
        fs3 = FileSet.FileSet(setIter=set3, root='/')
        fs1a = FileSet.FileSet(setIter=set1, root='/etc')

        self.assertNotIsInstance(fs1.__set__(), type(fs1))

        self.assertNotEqual(fs1, fs1a)

        self.assertEqual(fs1.union(fs2), fs1)
        self.assertEqual(fs1 | fs2, fs1)
        self.assertEqual(fs1.difference(fs2), fs3)
        self.assertEqual(fs1 - fs2, fs3)
        self.assertEqual(fs1.intersection(fs2), fs2)
        self.assertEqual(fs1 & fs2, fs2)

    def test_SetOperatorsOverRoot(self):
        set1 = set({'./somefile.txt'})
        set2 = set({'./somefile.txt',
                    './anotherfile.txt'})
        set3 = set({'etc/somefile.txt',
                    'var/anotherfile.txt',
                    'var/somefile.txt'})

        fs0 = FileSet.FileSet(setIter=set(), root='/')
        fs1 = FileSet.FileSet(setIter=set1, root='/etc')
        fs2 = FileSet.FileSet(setIter=set2, root='/var')
        fs3 = FileSet.FileSet(setIter=set3, root='/')
        fs4 = fs0 | fs1 | fs2

        with self.assertRaises(ValueError):
            fs1 | fs2

        self.assertIn('/etc/somefile.txt', fs1.normpath())

        self.assertEqual(fs3.root, fs4.root)
        self.assertEqual(fs3.updatefn, fs4.updatefn)

        self.assertEqual(fs3.__set__(), fs4.__set__())
        self.assertEqual(fs3, fs4)

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


class TestPackageSource(unittest.TestCase):
    def test_qfile(self):
        def qfile(src):
            with sp.Popen(["qfile {} | awk '{{print $1}}'".format(src)],
                          shell=True,
                          stdout=sp.PIPE) as proc:
                return proc.stdout.read().decode(
                    "utf-8").rstrip(os.linesep).split(os.linesep)

        def qlist(pkg):
            with sp.Popen(["qlist {}".format(pkg)],
                          shell=True,
                          stdout=sp.PIPE) as proc:
                return proc.stdout.read().decode(
                    "utf-8").rstrip(os.linesep).split(os.linesep)

        package = qfile("/bin/bash")[0]
        packageFiles = qlist(package)
        self.assertEqual(package, "app-shells/bash")
        self.assertIn("/bin/bash", packageFiles)

        fs0 = FileSet.FileSet(root='/',
                              setIter=set())
        fs1 = FileSet.FileSet(root='/',
                              setIter=set({"/bin/bash"}))
        fsp = FileSet.FileSet(root='/',
                              setIter=packageFiles)
        fsp2 = FileSet.FileSet(root='/',
                               setIter=set({"/bin/zsh"}))

        self.assertIn('/bin/bash', fs1)
        self.assertEqual(fs1 & fsp, fs1)
        self.assertEqual(fs1 | fsp, fsp)

        self.assertEqual(fs1 & fsp2, fs0)


if __name__ == '__main__':
    unittest.main()
