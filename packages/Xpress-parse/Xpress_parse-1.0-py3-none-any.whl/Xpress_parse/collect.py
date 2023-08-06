# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import sys
import json
import pandas as pd
from os.path import dirname, isdir


def ask_it(
        remove_add: str,
        record_pd: pd.DataFrame,
        selected: dict) -> str:
    """Ask the user whether a record is to be kept
    to (or removed from) the selection or not.

    Parameters
    ----------
    remove_add : str
        Whether to remove or add the record
    record_pd : pd.DataFrame
        Records table
    selected : dict
        Whether each record (key) is relevant (value = 1) or not (value = 0)

    Returns
    -------
    ret : str
        The string entered by the user for the current abstract
    """
    ret = input('Any record to %s? If yes, enter record number (e.g. 39 to %s '
                '"record#39") and press <Return>; if not, press <Return>\n' % (
                    remove_add, remove_add))
    if ret:
        record = 'record#%s' % ret
        if str(ret) in set(record_pd.index.astype(str)):
            if remove_add == 'add':
                selected[record] = (True, ['no_label'])
            elif record in selected:
                selected[record] = (False, None)
        else:
            print('\nRecord number "%s" not valid' % ret)

    return ret


def adding_something(
        remove_add: str,
        record_pd: pd.DataFrame,
        selected: dict) -> None:
    """Keeps asking the user whether the record is to be kept or removed.

    Parameters
    ----------
    remove_add : str
        Whether to remove or add the record
    record_pd : pd.DataFrame
        Records table
    selected : dict
        Whether each record (key) is relevant (value = 1) or not (value = 0)
    """
    ret = 'x'
    while ret:
        ret = ask_it(remove_add, record_pd, selected)


def write_out_progress(
        selected: dict,
        progress: str,
        cur_time: str) -> None:
    """Write the current progress in the file associated to the current search.

    Parameters
    ----------
    selected : dict
        Selected records
    progress : str
        Path to the file (no extension) that will contain the progress
        for the currently parsed WoS searches
    cur_time : str
        Formatted data and time of now
    """
    o_fp = '%s_%s.tsv' % (progress, cur_time)
    if not isdir(dirname(progress)):
        os.makedirs(dirname(progress))
    with open(o_fp, 'w') as o_json:
        json.dump(selected, o_json)
    print('Use the same exact command line to restart from here. Goodbye.')


def fix_version(selected: dict):
    """Update

    Parameters
    ----------
    selected : dict
        Selected studies

    Returns
    -------
    selected : dict
        Selected studies updated
    """
    selected = dict(
        (x, y) if isinstance(y, list) else (x, [y, 'not_available'])
        for x, y in selected.items())
    return selected


def make_progress_dir(progress_dir: str) -> bool:
    """Get and potentially create a directory that will
    contain the progress content.

    Parameters
    ----------
    progress_dir : str
        Path to the folder that will contain the progress for the
        currently parsed WoS searches

    Returns
    -------
    bool
        Whether the progress folder exists for the current search
    """
    if not isdir(progress_dir):
        os.makedirs(progress_dir)
        return False
    else:
        return True


def clear_output():
    """Clear the stdin and stdout on the Windows or Unix terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_query(labels: dict) -> str:
    """Get the query to be shown to the user under a record abstract.

    Parameters
    ----------
    labels : dict
        Mapping from keywords (keys) to labels (values)

    Returns
    -------
    query : str
        The query shown to the user
    """
    query = '>>> Exit\t: write "exit", "stop" or "quit" + press <Return>\n'
    query += '>>> Discard\t: press <Return>\n'
    query += '>>> Keep\t: write anything (or a keyword) + press <Return>'
    if labels:
        your_labels = '    [ Your labels:'
        for idx, (k, v) in enumerate(sorted(labels.items())):
            if idx:
                query += '\n%s %s -> %s' % (' ' * len(your_labels), k, v)
            else:
                query += '\n%s %s -> %s' % (your_labels, k, v)
        query += ' ]'
    query += '\n>>> '
    return query


def user_interact(
        user_record_pd: pd.DataFrame,
        selected: dict,
        progress: str,
        labels: dict,
        cur_time: str,
        rdx: int,
        r: int,
        n: int,
        row: pd.Series) -> tuple:
    """Collect the user input for a record.

    Parameters
    ----------
    user_record_pd : pd.DataFrame
        Table of the WoS search result(s) reduced to the records
        assigned to the current user
    selected : dict
        Selected records
    progress : str
        Path to the file (no extension) that will contain the progress
        for the currently parsed WoS searches
    labels : dict
        Mapping from keywords (keys) to labels (values)
    cur_time : str
        Formatted data and time of now
    rdx : int
        Iteration index
    r : int
        Index of the record in the original concatenated table
    n : int
        Total number of records for the current username
    row : pd.Series
        Record data

    Returns
    -------
    ret_val : tuple
        (bool, list) for whether to keep the record and with what labels
    """
    query = get_query(labels)
    ret = input('record#%s (%s/%s):\n%s\n%s et al. %s\n%s\n%s\n\n%s' % (
        r, rdx, n,
        '=' * 21,
        row['AU'].split(',')[0], row['TI'],
        '-' * 5,
        row['AB'],
        query
    ))

    if ret.lower() in ['exit', 'stop', 'quit']:
        # stopping asks to keep/remove records and writes progress
        add_and_remove(user_record_pd, selected)
        write_out_progress(selected, progress, cur_time)
        sys.exit(0)

    ret_val = (False, None)
    if ret:
        ret_val = (True, [labels.get(x, 'no_label') for x in str(ret).split()])
    return ret_val


def add_and_remove(user_record_pd, selected):
    """Ask the user whether the record is to be kept or removed

    Parameters
    ----------
    user_record_pd : pd.DataFrame
        Table of the WoS search result(s) reduced to the records
        assigned to the current user
    selected : dict
        Selected records
    """
    for add_remove in ['add', 'remove']:
        adding_something(add_remove, user_record_pd, selected)


def select_records(
        record_pd: pd.DataFrame,
        user: str,
        labels: dict,
        selected: dict,
        progress: str,
        cur_time: str) -> dict:
    """Interactively parsed the abstract and for each one, ask the user
    whether to stop, discard or keep it.
        If "stopped", then the progress so
    far is kept by writing a file (that is specific) for this search.
        If "discard", the abstract is labeled as False.
        If "kept", the abstract is labeled as True and potentially obtains
        one or more user-defined labels.

    Parameters
    ----------
    record_pd : pd.DataFrame
        Table of the WoS search result(s). A column indicating the source
        file name is added
    user : str
        Current username
    labels : dict
        Mapping from keywords (keys) to labels (values)
    selected : dict
        Selected records
    progress : str
        Path to the file (no extension) that will contain the progress
        for the currently parsed WoS searches
    cur_time : str
        Formatted data and time of now
    """
    # Subset the table to the records assigned to the current user
    user_record_pd = record_pd.loc[record_pd['PERSON'] == user]
    n = user_record_pd.shape[0]
    # Start parsing through the records
    for rdx, (r, row) in enumerate(user_record_pd.iterrows()):
        try:
            if 'record#%s' % r in selected:
                continue
            clear_output()
            selected['record#%s' % r] = user_interact(
                user_record_pd,
                selected,
                progress,
                labels,
                cur_time,
                rdx,
                r,
                n,
                row)
            clear_output()
        # using ctrl-c to exit asks to keep/remove records and writes progress
        except KeyboardInterrupt:
            add_and_remove(user_record_pd, selected)
            write_out_progress(selected, progress, cur_time)
            sys.exit(0)
    return selected
