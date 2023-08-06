# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import sys
import pandas as pd
from os.path import abspath, splitext


def get_output_fp(args: dict, user: str, cur_time: str) -> str:
    """Write the resulting selection to the output file.

    Parameters
    ----------
    args : dict
        All arguments, including:
            input_fps : tuple
                Path(s) to WoS search result(s)
            output_fp: str
                Selected records (default to xpress_records_YYYY-MM-DD.tsv)
    user : str
        Current username
    cur_time : str
        Formatted data and time of now

    Returns
    -------
    output_fp : str
        Output path
    """
    if args['output_fp']:
        output_fp = args['output_fp']
    else:
        cur_date = cur_time[:8]
        output_fp = splitext(args['input_fps'][0])[0] + '_xpressed_' + cur_date
        if user:
            output_fp += '_' + user + '.tsv'
        else:
            output_fp += '.tsv'
        output_fp = abspath(output_fp)
    return output_fp


def write_selection(
        output_fp: str,
        record_pd: pd.DataFrame,
        selected: dict) -> None:
    """Write the resulting selection to the output file.

    Parameters
    ----------
    output_fp : str
        Output path
    record_pd : pd.DataFrame
        Table of the WoS search result(s). A column indicating the source
        file name is added
    selected : dict
        Selected records
    """
    selected_studies = {
        int(k[7:]): '__'.join(b) for k, (a, b) in selected.items() if a}
    records_selection = record_pd.loc[sorted(selected_studies), :]

    if not len(records_selection):
        print('Nothing selected')
        sys.exit(0)

    records_selection['labels'] = [
        selected_studies[idx] for idx in records_selection.index]
    print('Written: %s' % output_fp)
    records_selection.to_csv(output_fp, index=False, sep='\t')
