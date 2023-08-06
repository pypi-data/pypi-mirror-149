# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np
import pandas as pd


def no_user(record_pd: pd.DataFrame) -> str:
    """Get an empty username if none was given in command line and also fill
    the "PERSON" column with empty string.

    Parameters
    ----------
    record_pd : pd.DataFrame
        Records table

    Returns
    -------
    user : str
        Current username
    """
    record_pd['PERSON'] = ''
    user = ''
    return user


def add_person_column(args: dict, record_pd: pd.DataFrame) -> None:
    """Add the "PERSON" column to the records table that contains on name
    per record. The names being split across the listed users.

    Parameters
    ----------
    args : dict
        All arguments, including:
            user : tuple
                User name(s)
    record_pd : pd.DataFrame
        Records table
    """
    users = sorted(set(args['user']))
    # Split the list of indices corresponding to the papers
    bins = list(np.linspace(0, 1, len(users), endpoint=False))
    bins.append(1)
    # use quantile cut to split index vector in equal-sized parts
    record_pd['PERSON'] = list(pd.qcut(record_pd.index, bins, labels=users))


def get_user(args: dict, record_pd: pd.DataFrame) -> str:
    """

    Parameters
    ----------
    args : dict
        All arguments, including:
            user : tuple
                User name(s)
    record_pd : pd.DataFrame
        Records table

    Returns
    -------
    user : str
        Current user name
    """
    add_person_column(args, record_pd)
    user = args['user'][0]
    return user


def get_user_chunks(args: dict, record_pd: pd.DataFrame) -> str:
    """Get the user work loads is a series of users is specified.

    Parameters
    ----------
    args : dict
        All arguments, including:
            input_fps : tuple
                Path(s) to WoS search result(s)
            output_fp: str
                Selected records (default to xpress_records_YYYY-MM-DD.tsv)
            user : tuple
                User name(s)
    record_pd : pd.DataFrame
        Records table

    Returns
    -------
    user : str
        Current username
    """
    # Define the list of people that will split the load amongst themselves
    if args['user']:
        user = get_user(args, record_pd)
    else:
        user = no_user(record_pd)
    return user


def show_users_allocation(
        record_pd: pd.DataFrame,
        user: str,
        selected: dict) -> None:
    """Print the number of records allocate to each user.

    Parameters
    ----------
    record_pd : pd.DataFrame
        Records table
    user : str
        Current username
    selected : dict
        Selected studies
    """
    if not user:
        n = len(record_pd)
        print("\n%s\nNumber of records to parse: %s\n%s" % ('-'*30, n, '-'*30))
    else:
        print("\n%s\nRecords allocated per person:\n%s" % ('-' * 29, '-' * 29))
        for u, n in record_pd['PERSON'].value_counts().sort_index().iteritems():
            m = '- %s: %s records' % (u, n)
            if u == user:
                m += ' (you'
                if selected:
                    m += ': %s records already parsed' % len(selected)
                m += ')'
            print(m)
