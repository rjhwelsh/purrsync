#!/usr/bin/env python3

# Copyright (c) 2018 Roger Welsh <rjhwelsh@gmail.com>

import unittest

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
