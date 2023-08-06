# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest
from unittest.mock import patch

from pandas.testing import assert_frame_equal
from Xpress_parse.users import *


class TestUsers(unittest.TestCase):

    def setUp(self) -> None:
        self.args = {'user': ['you', 'they', 'she']}
        self.record_pd = pd.DataFrame(
            [['1', 'file1'], ['2', 'file2'], ['3', 'file3']],
            columns=['AB', 'file'])
        self.record_user_pd = pd.DataFrame(
            [['1', 'file1', 'she'], ['2', 'file2', 'they'],
             ['3', 'file3', 'you']],
            columns=['AB', 'file', 'PERSON'])
        self.record_no_user_pd = pd.DataFrame(
            [['1', 'file1', ''], ['2', 'file2', ''], ['3', 'file3', '']],
            columns=['AB', 'file', 'PERSON'])

        self.args2 = {'user': ['she', 'you', 'they']}
        self.record2_pd = pd.DataFrame(
            [['1', 'file1'], ['2', 'file2'], ['3', 'file3'],
             ['4', 'file4'], ['5', 'file5'], ['6', 'file6'],
             ['7', 'file7'], ['8', 'file8']],
            columns=['AB', 'file'])
        self.record2_user_pd = pd.DataFrame(
            [['1', 'file1', 'she'], ['2', 'file2', 'she'],
             ['3', 'file3', 'she'], ['4', 'file4', 'they'],
             ['5', 'file5', 'they'], ['6', 'file6', 'you'],
             ['7', 'file7', 'you'], ['8', 'file8', 'you']],
            columns=['AB', 'file', 'PERSON'])
        self.record2_no_user_pd = pd.DataFrame(
            [['1', 'file1', ''], ['2', 'file2', ''], ['3', 'file3', ''],
             ['4', 'file4', ''], ['5', 'file5', ''], ['6', 'file6', ''],
             ['7', 'file7', ''], ['8', 'file8', '']],
            columns=['AB', 'file', 'PERSON'])

        self.args3 = {'user': ['they', 'you', 'she', 'she', 'she']}
        self.record3_pd = pd.DataFrame(
            [['1', 'file1'], ['2', 'file2'], ['3', 'file3'], ['4', 'file4']],
            columns=['AB', 'file'])
        self.record3_user_pd = pd.DataFrame(
            [['1', 'file1', 'she'], ['2', 'file2', 'she'],
             ['3', 'file3', 'they'], ['4', 'file4', 'you']],
            columns=['AB', 'file', 'PERSON'])
        self.record3_no_user_pd = pd.DataFrame(
            [['1', 'file1', ''], ['2', 'file2', ''], ['3', 'file3', ''],
             ['4', 'file4', '']],
            columns=['AB', 'file', 'PERSON'])

        hyphens = ('-' * 29, '-' * 29)
        self.exp = "\n%s\nRecords allocated per person:\n%s" % hyphens

    def test_add_person_column(self):
        add_person_column(self.args, self.record_pd)
        assert_frame_equal(self.record_pd, self.record_user_pd)
        add_person_column(self.args, self.record2_pd)
        assert_frame_equal(self.record2_pd, self.record2_user_pd)
        add_person_column(self.args, self.record3_pd)
        assert_frame_equal(self.record3_pd, self.record3_user_pd)

    def test_get_user(self):
        obs = get_user(self.args, self.record_pd)
        self.assertEqual(obs, 'you')
        obs = get_user(self.args2, self.record2_pd)
        self.assertEqual(obs, 'she')
        obs = get_user(self.args3, self.record3_pd)
        self.assertEqual(obs, 'they')

    def test_no_user(self):
        obs = no_user(self.record_pd)
        assert_frame_equal(self.record_pd, self.record_no_user_pd)
        self.assertEqual('', obs)
        obs = no_user(self.record2_pd)
        assert_frame_equal(self.record2_pd, self.record2_no_user_pd)
        self.assertEqual('', obs)
        obs = no_user(self.record3_pd)
        assert_frame_equal(self.record3_pd, self.record3_no_user_pd)
        self.assertEqual('', obs)


class TestUSerAlloc(unittest.TestCase):

    def setUp(self) -> None:
        self.record_pd = pd.DataFrame(
            [['1', 'file1', 'she'],
             ['2', 'file2', 'they'],
             ['3', 'file3', 'you']],
            columns=['AB', 'file', 'PERSON'])
        self.record2_pd = pd.DataFrame(
            [['1', 'file1', 'she'],
             ['2', 'file2', 'she'],
             ['3', 'file3', 'she'],
             ['4', 'file4', 'they'],
             ['5', 'file5', 'they'],
             ['6', 'file6', 'you'],
             ['7', 'file7', 'you'],
             ['8', 'file8', 'you']],
            columns=['AB', 'file', 'PERSON'])
        self.record3_pd = pd.DataFrame(
            [['1', 'file1', 'she'],
             ['2', 'file2', 'she'],
             ['3', 'file3', 'they'],
             ['4', 'file4', 'you']],
            columns=['AB', 'file', 'PERSON'])
        self.selected = {'1': (True, ['whatever'])}
        hyphens = ('-' * 29, '-' * 29)
        self.exp = "\n%s\nRecords allocated per person:\n%s" % hyphens

    @patch('builtins.print')
    def test_show_users_allocation(self, mock_print):
        show_users_allocation(self.record_pd, 'you', self.selected)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(print_out, self.exp)
        print_out = mock_print.call_args_list[1][0][0]
        self.assertEqual(print_out, '- she: 1 records')
        print_out = mock_print.call_args_list[2][0][0]
        self.assertEqual(print_out, '- they: 1 records')
        print_out = mock_print.call_args_list[3][0][0]
        self.assertEqual(print_out,
                         '- you: 1 records (you: 1 records already parsed)')

    @patch('builtins.print')
    def test_show_users_allocation2(self, mock_print):
        show_users_allocation(self.record2_pd, 'you', self.selected)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(print_out, self.exp)
        print_out = mock_print.call_args_list[1][0][0]
        self.assertEqual(print_out, '- she: 3 records')
        print_out = mock_print.call_args_list[2][0][0]
        self.assertEqual(print_out, '- they: 2 records')
        print_out = mock_print.call_args_list[3][0][0]
        self.assertEqual(print_out,
                         '- you: 3 records (you: 1 records already parsed)')

    @patch('builtins.print')
    def test_show_users_allocation3(self, mock_print):
        show_users_allocation(self.record3_pd, 'she', self.selected)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(print_out, self.exp)
        print_out = mock_print.call_args_list[1][0][0]
        self.assertEqual(print_out,
                         '- she: 2 records (you: 1 records already parsed)')
        print_out = mock_print.call_args_list[2][0][0]
        self.assertEqual(print_out, '- they: 1 records')
        print_out = mock_print.call_args_list[3][0][0]
        self.assertEqual(print_out, '- you: 1 records')

    @patch('builtins.print')
    def test_show_no_users_allocation(self, mock_print):
        show_users_allocation(self.record_pd, '', self.selected)
        print_out = mock_print.call_args_list[0][0][0]
        exp = "\n%s\nNumber of records to parse: 3\n%s" % ('-' * 30, '-' * 30)
        self.assertEqual(print_out, exp)

    @patch('builtins.print')
    def test_show_no_users_allocation2(self, mock_print):
        show_users_allocation(self.record2_pd, '', self.selected)
        print_out = mock_print.call_args_list[0][0][0]
        exp = "\n%s\nNumber of records to parse: 8\n%s" % ('-' * 30, '-' * 30)
        self.assertEqual(print_out, exp)

    @patch('builtins.print')
    def test_show_no_users_allocation3(self, mock_print):
        show_users_allocation(self.record3_pd, '', self.selected)
        print_out = mock_print.call_args_list[0][0][0]
        exp = "\n%s\nNumber of records to parse: 4\n%s" % ('-' * 30, '-' * 30)
        self.assertEqual(print_out, exp)


if __name__ == '__main__':
    unittest.main()
