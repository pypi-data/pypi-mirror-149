# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
from os.path import isfile


def read_records_fp(input_fp: str) -> pd.DataFrame:
    """
    Read one file of records returned by a WoS query.

    Parameters
    ----------
    input_fp : str
        Path to one WoS records file

    Returns
    -------
    records_pd : pd.DataFrame
        Table of the records
    """
    records_read = open(input_fp)
    records_lines = records_read.readlines()
    records_read.close()
    records = [x.strip().split('\t') for x in records_lines]
    records = pd.DataFrame(records[1:], columns=records[0])
    return records


def read_records_fps(args: dict) -> pd.DataFrame:
    """Read the WoS search results as tables and concatenate
    these into one main table.

    Parameters
    ----------
    args : dict
        All arguments, including:
            input_fps : tuple
                Path(s) to WoS search result(s)

    Returns
    -------
    record_pd : pd.DataFrame
        Table of the WoS search result(s)
        A column indicating the source file name is added
    """
    records = []
    for input_fp in args['input_fps']:
        if not isfile(input_fp):
            raise IOError('%s does not exist' % input_fp)
        record_pd = read_records_fp(input_fp)
        record_pd['file'] = input_fp
        records.append(record_pd)
    record_pd = pd.concat(records)
    record_pd.index = range(len(record_pd))
    return record_pd


def show_file_per_record(record_pd: pd.DataFrame) -> None:
    """Show the number of files in which the records may be shared.
    This is information before dropping these duplicates. Note that the file
    origin information will remain tracked.

    Parameters
    ----------
    record_pd : pd.DataFrame
        Table of the WoS search result(s)
        A column indicating the source file name is added
    """
    count_pd = record_pd[['AB', 'file']].groupby('AB').count()
    n = record_pd['file'].nunique()
    vc = count_pd.value_counts()
    if int(count_pd.max()) > 1:
        print('\n%s\nRedundant records found:\n%s' % ('-'*24, '-'*24))
        for i, j in dict(vc).items():
            m = '- %s records present in %s file' % (j, i[0])
            if i[0] > 1:
                m += 's'
            print(m)
    elif n > 1:
        print('\n%s\nRecords unique to the %s files\n%s' % ('-'*30, n, '-'*30))


def remove_empty_abstract(record_pd: pd.DataFrame) -> None:
    """Remove the row of the table that do not have an abstract and
    thus that will be skipped. This also reset the index.

    Parameters
    ----------
    record_pd : pd.DataFrame
        Table of the WoS search result(s)
    """
    to_drop = [x for x, row in record_pd.iterrows() if row['AB'] == '']
    if to_drop:
        record_pd.drop(index=to_drop, inplace=True)


def show_no_abstracts(record_pd: pd.DataFrame) -> None:
    """Show the recirds that do not have an abstract and thus that will be
    skipped.

    Parameters
    ----------
    record_pd : pd.DataFrame
        Table of the WoS search result(s)
        A column indicating the source file name is added

    Returns
    -------
    record_pd : pd.DataFrame
        Same table reduced to those records with available abstract
    """
    empty_pd = record_pd.loc[record_pd['AB'] == ''].copy()
    if empty_pd.shape[0]:
        print('\n%s\n%s abstracts empty:\n%s' % ('-'*19, len(empty_pd), '-'*19))
        no_record_dp = empty_pd.sort_values('PY')
        for rdx, (_, row) in enumerate(no_record_dp.iterrows()):
            print('[%s] %s, %s: %s' % (rdx, row['AU'].split(',')[0],
                                       row['PY'], row['TI'].lower()))


def update_file(record_pd: pd.DataFrame) -> None:
    """Updates the content of the "file" column so that abstracts
    present in multiple files have the full set of files.

    Parameters
    ----------
    record_pd : pd.DataFrame
        Same table reduced to those records with available abstract
    """
    file_per_ab = record_pd[['AB', 'file']].groupby('AB').apply(
        lambda x: ','.join(sorted(set(x['file'].values)))).to_dict()
    record_pd['file'] = [file_per_ab[x] for x in record_pd['AB']]
    record_pd.drop_duplicates(inplace=True)
    record_pd.index = range(len(record_pd))


def get_records(args: dict) -> pd.DataFrame:
    """Get the record tables by concatenating all input record tables.

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

    Returns
    -------
    record_pd : pd.DataFrame
        Table of the WoS search result(s). A column indicating the source
        file name is added
    """
    record_pd = read_records_fps(args)
    show_no_abstracts(record_pd)
    remove_empty_abstract(record_pd)
    show_file_per_record(record_pd)
    update_file(record_pd)
    return record_pd
