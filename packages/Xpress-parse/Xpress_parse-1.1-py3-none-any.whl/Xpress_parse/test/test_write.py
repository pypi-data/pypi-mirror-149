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

import pandas as pd
from pandas.testing import assert_frame_equal
import pkg_resources
from datetime import datetime

from Xpress_parse.write import *


class TestWrite(unittest.TestCase):

    def setUp(self) -> None:
        self.root = pkg_resources.resource_filename('Xpress_parse', 'test')
        self.tsv = '%s/input.tsv' % self.root
        self.args = {'input_fps': ('/a/b.txt',), 'output_fp': '/some/path.tsv'}
        self.record_pd = pd.DataFrame(
            [['1', 'f1', 'you'],
             ['2', 'f2', 'you'],
             ['3', 'f3', 'you'],
             ['4', 'f4', 'you'],
             ['5', 'f5', 'you']],
            columns=['AB', 'file', 'PERSON'],
            index=[0, 1, 2, 3, 4])
        self.output_fp = '%s/out.tsv' % pkg_resources.resource_filename(
            'Xpress_parse', 'test')

    @patch('builtins.print')
    def test_write_no_selection(self, mock_print):
        selected = {'record#0': (False, None),
                    'record#1': (False, None),
                    'record#2': (False, None),
                    'record#3': (False, None),
                    'record#4': (False, None)}

        with self.assertRaises(SystemExit) as cm:
            write_selection(self.output_fp, self.record_pd, selected)
        self.assertEqual(cm.exception.code, 0)

        self.assertFalse(os.path.isfile(self.output_fp))

        exp = 'Nothing selected'
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(exp, print_out)

    @patch('builtins.print')
    def test_write_selection(self, mock_print):
        selected = {'record#0': (True, ['no_label']),
                    'record#1': (False, None),
                    'record#2': (False, None),
                    'record#3': (False, None),
                    'record#4': (False, None)}
        out_pd = pd.DataFrame([['1', 'f1', 'you', 'no_label']],
                              columns=['AB', 'file', 'PERSON', 'labels'],
                              index=[0])
        write_selection(self.output_fp, self.record_pd, selected)
        print_out = mock_print.call_args_list[0][0][0]

        self.assertTrue(os.path.isfile(self.output_fp))

        obs_pd = pd.read_csv(self.output_fp, sep='\t', dtype=str)
        assert_frame_equal(out_pd, obs_pd)

        exp = 'Written: %s' % self.output_fp
        self.assertEqual(exp, print_out)

    @patch('builtins.print')
    def test_write_selection_filled(self, mock_print):
        selected = {'record#0': (False, None),
                    'record#1': (True, ['no_label']),
                    'record#2': (True, ['a']),
                    'record#3': (True, ['a', 'b']),
                    'record#4': (False, None)}
        out_pd = pd.DataFrame([['2', 'f2', 'you', 'no_label'],
                               ['3', 'f3', 'you', 'a'],
                               ['4', 'f4', 'you', 'a__b']],
                              columns=['AB', 'file', 'PERSON', 'labels'],
                              index=[0, 1, 2])
        write_selection(self.output_fp, self.record_pd, selected)
        print_out = mock_print.call_args_list[0][0][0]

        self.assertTrue(os.path.isfile(self.output_fp))

        obs_pd = pd.read_csv(self.output_fp, sep='\t', dtype=str)
        assert_frame_equal(out_pd, obs_pd)

        exp = 'Written: %s' % self.output_fp
        self.assertEqual(exp, print_out)

    def test_get_output_fp(self):
        obs = get_output_fp(self.args, 'whatever', '')
        self.assertEqual('/some/path.tsv', obs)

    def test_get_output_fp_exist(self):
        self.args['output_fp'] = None
        cur_date = datetime.now().strftime("%Y%m%d")
        obs = get_output_fp(self.args, '', cur_date)
        exp = '/a/b_xpressed_%s.tsv' % cur_date
        self.assertEqual(exp, obs)

    def test_get_output_fp_user(self):
        self.args['output_fp'] = None
        cur_date = datetime.now().strftime("%Y%m%d")
        obs = get_output_fp(self.args, 'USER', cur_date)
        exp = '/a/b_xpressed_%s_USER.tsv' % cur_date
        self.assertEqual(exp, obs)

    def tearDown(self) -> None:
        if os.path.isfile(self.output_fp):
            os.remove(self.output_fp)


if __name__ == '__main__':
    unittest.main()
