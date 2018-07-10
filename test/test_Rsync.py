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

    def test_Rsync(self):
        """ Tests the default use case for Rsync. """

        with tempfile.TemporaryDirectory() as src1:
            src = src1 + os.sep
            # Temporary files
            a = tempfile.NamedTemporaryFile(mode="r", dir=src, delete=False)
            b = tempfile.NamedTemporaryFile(mode="r", dir=src, delete=False)
            c = tempfile.NamedTemporaryFile(mode="r", dir=src, delete=False)
            d = tempfile.NamedTemporaryFile(mode="r", dir=src, delete=False)

            fileList = [FileSet.removePrefix(i.name, src)
                        for i in [a, b, c, d]]

            packageSet = {
                "pkg_{}".format(key): FileSet.FileSet(setIter=[key],
                                                      root=src)
                for key in fileList[0:3]
            }

            ignoreSet = FileSet.FileSet(setIter=[fileList[2]],
                                        root=src)

            mainSet = FileSet.FileSet(setIter=fileList,
                                      root=src)

            with tempfile.TemporaryDirectory() as dest:
                rs1 = Rsync.Rsync(src, dest,
                                  mainSet=mainSet,
                                  ignoreSet=ignoreSet,
                                  packageSet=packageSet,
                                  rsyncArgs="-v")
                rs1.prepareDest()

                rs1.rsyncMain()

                destroot = os.path.join(
                    dest,
                    rs1.MAIN,
                    rs1.ROOT)

                self.assertTrue(
                    os.path.exists(destroot),
                    msg="{} does not exist!".format(
                        destroot))

                destfiles = [os.path.join(
                    destroot,
                    f)
                    for f in fileList]

                for df in destfiles[0:2] + [destfiles[3]]:
                    self.assertTrue(
                        os.path.exists(df),
                        msg="{} does not exist!".format(
                            df))

                for pkg, proc in rs1.rsyncPackages():
                    pass

                pkgroot = os.path.join(dest, rs1.PACKAGE)

                destroot = [
                    os.path.join(
                        pkgroot,
                        'pkg_{}'.format(key),
                        rs1.ROOT)
                    for key in fileList[0:3]]

                for i, d in enumerate(destroot):
                    self.assertTrue(
                        os.path.exists(d),
                        msg="{} does not exist!".format(
                            d))

                    destfile = os.path.join(
                        d,
                        fileList[i])
                    if i < 2:
                        self.assertTrue(
                            os.path.exists(destfile),
                            msg="{} does not exist!".format(
                                destfile))

                rs1.rsyncOrphans()

                orproot = os.path.join(dest, rs1.ORPHAN, rs1.ROOT)
                orpfile = os.path.join(orproot, fileList[3])

                self.assertTrue(
                    os.path.exists(orproot))

                self.assertTrue(
                    os.path.exists(orpfile))
