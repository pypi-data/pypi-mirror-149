# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import unittest
import pkg_resources

from Xpress_parse.progress import *


class Test(unittest.TestCase):

    def setUp(self) -> None:
        test_folder = pkg_resources.resource_filename('Xpress_parse', 'test')
        self.selected = {}
        self.prog = '%s/rad' % test_folder
        self.fp1 = '%s_21.tsv' % self.prog
        self.fp2 = '%s_22.tsv' % self.prog
        self.input_fps = (self.fp1, self.fp2,)
        with open(self.fp1, 'w') as o:
            o.write('{"record#0": [false, null], "record#1": [false, "a"]}')
        with open(self.fp2, 'w') as o:
            o.write('{"record#2": [false, null], "record#1": [false, "b"]}')

        self.args = {'input_fps': ('/a/b.tsv', '/c/d.tsv',)}
        self.hashlib = hashlib.sha224('/a/b.tsv/c/d.tsv'.encode()).hexdigest()
        self.prog_dir = '/a/.xpress/' + self.hashlib

    def test_get_progress_files(self):
        get_progress_files(self.prog, self.selected)
        exp = {"record#2": [False, None], "record#1": [False, "b"]}
        self.assertEqual(self.selected, exp)

    def test_get_progress_files_fp1(self):
        os.remove(self.fp2)  # suppress most recent progress
        get_progress_files(self.prog, self.selected)
        exp = {"record#0": [False, None], "record#1": [False, "a"]}
        self.assertEqual(self.selected, exp)

    def test_get_progress_files_none(self):
        os.remove(self.fp2)  # suppress all
        os.remove(self.fp1)  # suppress all
        get_progress_files(self.prog, self.selected)
        exp = {}
        self.assertEqual(exp, self.selected)

    def test_get_progress_base(self):
        obs = get_progress_base(self.args)
        self.assertEqual(self.prog_dir, obs)

    def test_read_past_progress(self):
        selected, progress = read_past_progress(self.args)
        self.assertEqual(self.prog_dir, progress)
        self.assertEqual({}, selected)

    def test_read_past_progress_sel(self):
        selected, progress = read_past_progress(self.args)
        self.assertEqual(self.prog_dir, progress)

    def tearDown(self) -> None:
        if os.path.isfile(self.fp1):
            os.remove(self.fp1)
        if os.path.isfile(self.fp2):
            os.remove(self.fp2)


if __name__ == '__main__':
    unittest.main()
