# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest
from unittest.mock import patch
import pkg_resources
from os.path import isfile

from Xpress_parse.collect import *


class TestCollect(unittest.TestCase):

    def setUp(self) -> None:
        self.record_pd = pd.DataFrame(
            [['1', 'f1', 'she'], ['2', 'f2', 'they'], ['3', 'f3', 'you']],
            columns=['AB', 'file', 'PERSON'], index=[0, 1, 2])

        self.selected = {'record#2': (True, ['no_label'])}

        self.query = '>>> Exit\t: write "exit", "stop" or "quit" + press '
        self.query += '<Return>\n>>> Discard\t: press <Return>\n>>> Keep\t'
        self.query += ': write anything (or a keyword) + press <Return>'

        test_folder = pkg_resources.resource_filename('Xpress_parse', 'test')
        self.progress_dir = '%s/progress_folder' % test_folder
        self.progress = '%s/rad' % self.progress_dir
        self.progress_fp = '%s_TIME.tsv' % self.progress

        self.row = pd.Series(['a', 'b', 'c'], index=['AU', 'TI', 'AB'])

    @patch('builtins.input', return_value='')
    def test_user_interact_no_return(self, mock_input):
        obs = user_interact(self.record_pd, self.selected, self.progress,
                            {'1': 'a'}, 'TIME', 0, 0, 1, self.row)
        exp = (False, None)
        self.assertEqual(exp, obs)

    @patch('builtins.input', return_value='5')
    def test_user_interact_no_label(self, mock_input):
        obs = user_interact(self.record_pd, self.selected, self.progress,
                            {'1': 'a'}, 'TIME', 0, 0, 1, self.row)
        exp = (True, ['no_label'])
        self.assertEqual(exp, obs)

    @patch('builtins.input', return_value='1')
    def test_user_interact_label(self, mock_input):
        obs = user_interact(self.record_pd, self.selected, self.progress,
                            {'1': 'a'}, 'TIME', 0, 0, 1, self.row)
        exp = (True, ['a'])
        self.assertEqual(exp, obs)

    # the two last '' are to end the loop are the user is asked to add/remove
    @patch('builtins.input', side_effect=['exit', '', ''])
    def test_user_interact(self, mock_input):
        with self.assertRaises(SystemExit) as cm:
            user_interact(self.record_pd, self.selected, self.progress,
                          {'1': 'a'}, 'TIME', 0, 0, 1, self.row)
        self.assertEqual(cm.exception.code, 0)

    @patch('builtins.input', side_effect=['exit', '0', '1', '2', '', '1', ''])
    def test_user_interact_mixed(self, mock_input):
        with self.assertRaises(SystemExit) as cm:
            user_interact(self.record_pd, self.selected, self.progress,
                          {'1': 'a'}, 'TIME', 0, 0, 1, self.row)
        self.assertEqual(cm.exception.code, 0)
        exp = {'record#0': (True, ['no_label']),
               'record#1': (False, None),
               'record#2': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)

    @patch('builtins.print')
    def test_write_out_progress(self, mock_print):
        write_out_progress({'1': (False, None)}, self.progress, 'TIME')
        with open(self.progress_fp) as f:
            for line in f:
                obs = line.strip()
        self.assertEqual('{"1": [false, null]}', obs)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(
            print_out,
            'Use the same exact command line to restart from here. Goodbye.')

        select = {'1': (False, None), '2': (True, ['a', 'b'])}
        write_out_progress(select, self.progress, 'TIME')
        with open(self.progress_fp) as f:
            for line in f:
                obs = line.strip()
        self.assertEqual('{"1": [false, null], "2": [true, ["a", "b"]]}', obs)
        print_out = mock_print.call_args_list[0][0][0]
        self.assertEqual(
            print_out,
            'Use the same exact command line to restart from here. Goodbye.')

    @patch('builtins.input', return_value='')
    def test_ask_it_add_no_ret(self, mock_input):
        obs = ask_it('add', self.record_pd, self.selected)
        self.assertEqual({'record#2': (True, ['no_label'])}, self.selected)
        self.assertEqual('', obs)
        obs = ask_it('remove', self.record_pd, self.selected)
        self.assertEqual({'record#2': (True, ['no_label'])}, self.selected)
        self.assertEqual('', obs)

    @patch('builtins.input', return_value='not_in')
    def test_ask_it_add_not_in(self, mock_input):
        obs = ask_it('add', self.record_pd, self.selected)
        self.assertEqual({'record#2': (True, ['no_label'])}, self.selected)
        self.assertEqual('not_in', obs)

    @patch('builtins.input', return_value='not_in')
    def test_ask_it_remove_not_in(self, mock_input):
        obs = ask_it('add', self.record_pd, self.selected)
        self.assertEqual({'record#2': (True, ['no_label'])}, self.selected)
        self.assertEqual('not_in', obs)

    @patch('builtins.input', return_value='1')
    def test_ask_it_add(self, mock_input):
        obs = ask_it('add', self.record_pd, self.selected)
        exp = {'record#2': (True, ['no_label']),
               'record#1': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)
        self.assertEqual('1', obs)

    @patch('builtins.input', return_value='1')
    def test_ask_it_change(self, mock_input):
        obs = ask_it('remove', self.record_pd, self.selected)
        exp = {'record#2': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)
        self.assertEqual('1', obs)

    @patch('builtins.input', return_value='1')
    def test_ask_it_remove_nothing(self, mock_input):
        obs = ask_it('remove', self.record_pd, self.selected)
        exp = {'record#2': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)
        self.assertEqual('1', obs)

    @patch('builtins.input', return_value='2')
    def test_ask_it_remove(self, mock_input):
        obs = ask_it('remove', self.record_pd, self.selected)
        exp = {'record#2': (False, None)}
        self.assertEqual(exp, self.selected)
        self.assertEqual('2', obs)

    @patch('builtins.input', side_effect=['not_in', ''])
    def test_adding_something_add_no_ret(self, mock_input):
        adding_something('add', self.record_pd, self.selected)
        self.assertEqual({'record#2': (True, ['no_label'])}, self.selected)

    @patch('builtins.input', side_effect=['not_in', ''])
    def test_adding_something_remove_no_ret(self, mock_input):
        adding_something('remove', self.record_pd, self.selected)
        self.assertEqual({'record#2': (True, ['no_label'])}, self.selected)

    @patch('builtins.input', side_effect=['5', ''])
    def test_adding_something_add_not_in(self, mock_input):
        adding_something('add', self.record_pd, self.selected)
        self.assertEqual({'record#2': (True, ['no_label'])}, self.selected)

    @patch('builtins.input', side_effect=['1', ''])
    def test_adding_something_add(self, mock_input):
        adding_something('add', self.record_pd, self.selected)
        exp = {'record#2': (True, ['no_label']),
               'record#1': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)

    @patch('builtins.input', side_effect=['1', ''])
    def test_adding_something_change(self, mock_input):
        adding_something('remove', self.record_pd, self.selected)
        exp = {'record#2': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)

    @patch('builtins.input', side_effect=['1', ''])
    def test_adding_something_remove_nothing(self, mock_input):
        adding_something('remove', self.record_pd, self.selected)
        exp = {'record#2': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)

    @patch('builtins.input', side_effect=['2', ''])
    def test_adding_something(self, mock_input):
        adding_something('remove', self.record_pd, self.selected)
        exp = {'record#2': (False, None)}
        self.assertEqual(exp, self.selected)

    @patch('builtins.input', side_effect=['0', '1', '3', '4', ''])
    def test_adding_something_add_multiple(self, mock_input):
        adding_something('add', self.record_pd, self.selected)
        exp = {'record#0': (True, ['no_label']),
               'record#1': (True, ['no_label']),
               'record#2': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)

    @patch('builtins.input', side_effect=['0', '1', '2', '3', '4', ''])
    def test_adding_something_remove_multiple(self, mock_input):
        adding_something('remove', self.record_pd, self.selected)
        exp = {'record#2': (False, None)}
        self.assertEqual(exp, self.selected)

    @patch('builtins.input', side_effect=['0', '1', '', '2', '3', '4', ''])
    def test_add_and_remove(self, mock_input):
        self.selected = {'record#2': (True, ['no_label'])}
        add_and_remove(self.record_pd, self.selected)
        exp = {'record#0': (True, ['no_label']),
               'record#1': (True, ['no_label']),
               'record#2': (False, None)}
        self.assertEqual(exp, self.selected)

    @patch('builtins.input', side_effect=['0', '1', '2', '', '1', ''])
    def test_add_and_remove_mixed(self, mock_input):
        self.selected = {'record#2': (True, ['no_label'])}
        add_and_remove(self.record_pd, self.selected)
        exp = {'record#0': (True, ['no_label']),
               'record#1': (False, None),
               'record#2': (True, ['no_label'])}
        self.assertEqual(exp, self.selected)

    def test_get_query(self):
        obs = get_query({'a': '1'})
        self.query += '\n    [ Your labels: a -> 1 ]\n>>> '
        self.assertEqual(self.query, obs)

    def test_get_query2(self):
        obs = get_query({'a': '1', 'b': 2})
        self.query += '\n    [ Your labels: a -> 1'
        self.query += '\n                   b -> 2 ]\n>>> '
        self.assertEqual(self.query, obs)

    def tearDown(self) -> None:
        if isfile(self.progress_fp):
            os.remove(self.progress_fp)
        if isdir(self.progress_dir):
            os.rmdir(self.progress_dir)


if __name__ == '__main__':
    unittest.main()
