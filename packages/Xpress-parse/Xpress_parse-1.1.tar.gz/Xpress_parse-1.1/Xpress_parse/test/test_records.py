# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest
from unittest.mock import patch

import os
import pkg_resources
from pandas.testing import assert_frame_equal

from Xpress_parse.records import *


class TestUpdateFile(unittest.TestCase):

    def setUp(self) -> None:
        self.pd_redundancy = pd.DataFrame(
            [['1', 'file1a'],       # same 4 abstracts "1"
                ['1', 'file2'],
                ['1', 'file3'],
                ['1', 'file1b'],
             ['2', 'file2'],        # one abstract "2"
             ['3', 'file3a'],       # same 3 abstracts "3"
                ['3', 'file3b'],
                ['3', 'file3c']],
            columns=['AB', 'file'])
        # no redundancy
        self.pd_no_redundancy = pd.DataFrame(
            [['1', 'file1'],
             ['2', 'file2'],
             ['3', 'file3']],
            columns=['AB', 'file'])

    def test_update_file_redundancy(self):
        update_file(self.pd_redundancy)
        exp = pd.DataFrame(
            [['1', 'file1a,file1b,file2,file3'],
             ['2', 'file2'],
             ['3', 'file3a,file3b,file3c']],
            columns=['AB', 'file'])
        assert_frame_equal(self.pd_redundancy, exp)

    def test_update_file_no_redundancy(self):
        update_file(self.pd_no_redundancy)
        exp = pd.DataFrame(
            [['1', 'file1'],
             ['2', 'file2'],
             ['3', 'file3']],
            columns=['AB', 'file'])
        assert_frame_equal(self.pd_no_redundancy, exp)


class TestShowFilePerRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.pd_single = pd.DataFrame(
            [['1', 'file1'], ['2', 'file1'], ['3', 'file1']],
            columns=['AB', 'file'])

        dashes = ('-' * 24, '-' * 24)
        self.pd_1_exp = '\n%s\nRedundant records found:\n%s' % dashes
        self.pd_1_exp_1 = '- 3 records present in 2 files'
        self.pd_1 = pd.DataFrame(
            [['1', 'file1'], ['2', 'file1'], ['3', 'file1'],
             ['1', 'file2'], ['2', 'file2'], ['3', 'file2']],
            columns=['AB', 'file'])

        dashes = ('-' * 24, '-' * 24)
        self.pd_2_exp = '\n%s\nRedundant records found:\n%s' % dashes
        self.pd_2_exp_1 = '- 3 records present in 1 file'
        self.pd_2_exp_2 = '- 2 records present in 2 files'
        self.pd_2 = pd.DataFrame(
            [['1', 'file1'], ['2', 'file1'], ['3', 'file1'], ['4', 'file1'],
             ['4', 'file2'], ['5', 'file1'], ['5', 'file3']],
            columns=['AB', 'file'])

        dashes = ('-' * 30, '-' * 30)
        self.pd_exp = '\n%s\nRecords unique to the 3 files\n%s' % dashes
        self.pd = pd.DataFrame(
            [['1', 'file1'], ['2', 'file2'], ['3', 'file3']],
            columns=['AB', 'file'])

    def test_show_file_per_record_single(self):
        self.assertIsNone(show_file_per_record(self.pd_single))

    @patch('builtins.print')
    def test_show_file_per_record_1(self, mock_print):
        show_file_per_record(self.pd_1)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(print_out, self.pd_1_exp)
        print_out = mock_print.call_args_list[1][0][0]
        self.assertEqual(print_out, self.pd_1_exp_1)
        with self.assertRaises(IndexError):
            print_out = mock_print.call_args_list[2][0][0]

    @patch('builtins.print')
    def test_show_file_per_record_2(self, mock_print):
        show_file_per_record(self.pd_2)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(print_out, self.pd_2_exp)
        print_out = mock_print.call_args_list[1][0][0]
        self.assertEqual(print_out, self.pd_2_exp_1)
        print_out = mock_print.call_args_list[2][0][0]
        self.assertEqual(print_out, self.pd_2_exp_2)
        with self.assertRaises(IndexError):
            print_out = mock_print.call_args_list[3][0][0]

    @patch('builtins.print')
    def test_show_file_per_record(self, mock_print):
        show_file_per_record(self.pd)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(print_out, self.pd_exp)


class TestRemoveEmptyAbstract(unittest.TestCase):

    def setUp(self) -> None:
        self.nothing = pd.DataFrame(
            [['1', 'file1'], ['2', 'file1'], ['3', 'file1']],
            columns=['AB', 'file'])
        self.after = pd.DataFrame(
            [['1', 'file1'], ['2', 'file1'], ['3', 'file1']],
            columns=['AB', 'file'])

        self.empty = pd.DataFrame(
            [['', 'file1'], ['', 'file1'], ['3', 'file1']],
            columns=['AB', 'file'])
        self.after_empty = pd.DataFrame(
            [['3', 'file1']], columns=['AB', 'file'], index=[2])

    def test_remove_empty_abstract(self):
        remove_empty_abstract(self.nothing)
        assert_frame_equal(self.nothing, self.after)
        remove_empty_abstract(self.empty)
        assert_frame_equal(self.empty, self.after_empty)


class TestShowNoAbstracts(unittest.TestCase):

    def setUp(self) -> None:
        self.missing = pd.DataFrame(
            [['', 'file1', 2, 'B,b', 'Title2'],
             ['', 'file1', 1, 'A,a', 'TITLE1'],
             ['3', 'file1', 3, 'C,c', 'Title3']],
            columns=['AB', 'file', 'PY', 'AU', 'TI'], index=[4, 1, 1])

        dashes = ('-' * 19, '-' * 19)
        self.missing_exp = '\n%s\n2 abstracts empty:\n%s' % dashes
        self.missing_exp_1 = '[0] A, 1: title1'
        self.missing_exp_2 = '[1] B, 2: title2'

    @patch('builtins.print')
    def test_show_no_abstracts(self, mock_print):
        show_no_abstracts(self.missing)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(print_out, self.missing_exp)
        print_out = mock_print.call_args_list[1][0][0]
        self.assertEqual(print_out, self.missing_exp_1)
        print_out = mock_print.call_args_list[2][0][0]
        self.assertEqual(print_out, self.missing_exp_2)
        with self.assertRaises(IndexError):
            print_out = mock_print.call_args_list[3][0][0]


class TestReadRecordsFp(unittest.TestCase):

    def setUp(self) -> None:
        self.data = [['A', 'B', 'C', 'D'],
                     ['A1', 'B1', 'C1', 'D1'],
                     ['A2', 'B2', 'C2', 'D2']]
        self.root = pkg_resources.resource_filename('Xpress_parse', 'test')
        self.test_fp1 = '%s/test_fp1' % self.root
        self.test_fp2 = '%s/test_fp2' % self.root
        self.data_fps = [self.test_fp1, self.test_fp2]
        self.args = {'input_fps': self.data_fps}
        for data_fp in self.data_fps:
            with open(data_fp, 'w') as o:
                for data in self.data:
                    o.write('%s\n' % '\t'.join(data))
        self.not_exists = ['not_a_file.tsv']
        self.args_not_exists = {'input_fps': self.not_exists}

    def test_read_records_fp(self):
        obs = read_records_fp(self.data_fps[0])
        exp = pd.DataFrame([['A1', 'B1', 'C1', 'D1'],
                            ['A2', 'B2', 'C2', 'D2']],
                           columns=['A', 'B', 'C', 'D'])
        assert_frame_equal(exp, obs)

    def test_read_records_fps(self):
        obs = read_records_fps(self.args)
        exp = pd.DataFrame([['A1', 'B1', 'C1', 'D1', self.test_fp1],
                            ['A2', 'B2', 'C2', 'D2', self.test_fp1],
                            ['A1', 'B1', 'C1', 'D1', self.test_fp2],
                            ['A2', 'B2', 'C2', 'D2', self.test_fp2]],
                           columns=['A', 'B', 'C', 'D', 'file'])
        assert_frame_equal(exp, obs)

        with self.assertRaises(IOError):
            read_records_fps(self.args_not_exists)

    def tearDown(self) -> None:
        for data_fp in self.data_fps:
            os.remove(data_fp)


if __name__ == '__main__':
    unittest.main()
