#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import unittest
import tempfile
import os

import parsync.Rsync as Rsync
import parsync.FileSet as FileSet


class TestRsync(unittest.TestCase):
    def test_Init(self):
        m1 = FileSet.FileSet()
        i1 = FileSet.FileSet()
        p1 = dict()
        rA = ""

        rs1 = Rsync.Rsync(mainSet=m1,
                          ignoreSet=i1,
                          packageSet=p1,
                          rsyncArgs=rA)

        self.assertEqual(rs1.mainSet, m1)
        self.assertEqual(rs1.ignoreSet, i1)
        self.assertEqual(rs1.packageSet, p1)
        self.assertEqual(rs1.rsyncArgs, rA)

    def test_which(self):
        rs1 = Rsync.Rsync()
        self.assertEqual(rs1.which(), "/usr/bin/rsync")

    def test_prepareDest(self):
        with tempfile.TemporaryDirectory() as dest:
            rs1 = Rsync.Rsync(destination=dest)
            rs1.prepareDest()

            # Test defaults
            self.assertTrue(
                os.path.isdir(
                    os.path.join(dest,
                                 rs1.MAIN,
                                 rs1.ROOT)))

            self.assertTrue(
                os.path.isdir(
                    os.path.join(dest,
                                 rs1.ORPHAN,
                                 rs1.ROOT)))
            self.assertTrue(
                os.path.isdir(
                    os.path.join(dest,
                                 rs1.PACKAGE)))

            self.assertFalse(
                os.listdir(
                    os.path.join(
                        dest,
                        rs1.PACKAGE)))

            # Test with packages
            pkgname = 'somepackage'
            catname = 'category'
            rs2 = Rsync.Rsync(destination=dest,
                              packageSet={pkgname:
                                          FileSet.FileSet(),

                                          os.sep.join([catname,
                                                       pkgname]):
                                          FileSet.FileSet()})
            rs2.prepareDest()
            pkgpath = os.path.join(dest, rs1.PACKAGE, pkgname)
            catpath = os.path.join(dest, rs1.PACKAGE, catname)
            catpkgpath = os.path.join(catpath, pkgname)

            for i in [pkgpath, catpath, catpkgpath]:
                self.assertTrue(
                    os.path.isdir(
                        i))

            # Test ssh not implemented
            with self.assertRaises(NotImplementedError):
                rs3 = Rsync.Rsync(destination="192.168.1.1:" + dest)
                rs3.prepareDest()
