# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import unittest
from unittest.mock import patch
import pkg_resources

from Xpress_parse.labels import *


class TestLabels(unittest.TestCase):

    def setUp(self) -> None:
        self.root = pkg_resources.resource_filename('Xpress_parse', 'test')
        self.tsv = '%s/labels.tsv' % self.root
        self.labels = {1: 'a', 2: 'b', 3: 'c'}
        with open(self.tsv, 'w') as o:
            for k, v in self.labels.items():
                o.write('%s\t%s\n' % (k, v))
        self.tsv_extra = '%s/labels_extra.tsv' % self.root
        with open(self.tsv_extra, 'w') as o:
            for k, v in self.labels.items():
                o.write('%s\t%s\tuseless\n' % (k, v))

    def test_read_labels(self):
        obs = read_labels(self.tsv)
        self.assertEqual(self.labels, obs)
        obs = read_labels(self.tsv_extra)
        self.assertEqual(self.labels, obs)

    @patch('builtins.input', side_effect=['1', '2', '3', '4', ''])
    def test_collect_labels_1(self, input):
        obs = collect_labels()
        self.assertEqual({'1': '2', '3': '4'}, obs)

    @patch('builtins.input', side_effect=['1', '2', '3', ''])
    def test_collect_labels_2(self, input):
        obs = collect_labels()
        self.assertEqual({'1': '2'}, obs)

    @patch('builtins.input', side_effect=[''])
    def test_collect_labels_3(self, input):
        obs = collect_labels()
        self.assertEqual({}, obs)

    @patch('builtins.input', side_effect=['1', '2', '1', '3', ''])
    def test_collect_labels_4(self, input):
        obs = collect_labels()
        self.assertEqual({'1': '3'}, obs)

    def test_curate_labels(self):
        labels = {'what': 'ever'}
        exp = {'what': 'ever'}
        curate_labels(labels)
        self.assertEqual(labels, exp)

        labels = {}
        exp = {}
        curate_labels(labels)
        self.assertEqual(labels, exp)

        labels = {'exit': 'is_wrong'}
        exp = {}
        curate_labels(labels)
        self.assertEqual(labels, exp)

        labels = {'exit': 'is_wrong', 'quit': 'is_wrong'}
        exp = {}
        curate_labels(labels)
        self.assertEqual(labels, exp)

        labels = {'exit': 'is_wrong', 'quit': 'is_wrong', 'stop': 'is_wrong'}
        exp = {}
        curate_labels(labels)
        self.assertEqual(labels, exp)

    def tearDown(self) -> None:
        os.remove(self.tsv)
        os.remove(self.tsv_extra)


if __name__ == '__main__':
    unittest.main()
