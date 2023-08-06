# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from datetime import datetime
from Xpress_parse.records import get_records
from Xpress_parse.users import get_user_chunks, show_users_allocation
from Xpress_parse.labels import get_labels
from Xpress_parse.collect import select_records
from Xpress_parse.progress import read_past_progress
from Xpress_parse.write import get_output_fp, write_selection


def xpress(**args) -> None:
    """
    Main script to collect the records, parse them and interact with the
    user to make a selection that potentially can be labelled.

    Parameters
    ----------
    args : dict
        All arguments, including:
            input_fps : tuple
                Path(s) to WoS search result(s)
            output_fp: str
                Selected records (default to xpress_records_YYYY-MM-DD.tsv)
            user : tuple
                Username(s)
            labels_fp : str
                Path to file with 2 tab-separated columns: keywords and labels
    """
    # Get the record tables by concatenating all input record tables
    record_pd = get_records(args)
    # Get the user work loads is a series of users is specified
    user = get_user_chunks(args, record_pd)
    # Get the labels from file or from user interactively
    labels = get_labels(args)
    # Check whether some selection was already made and if yes collect progress
    selected, progress = read_past_progress(args)
    # Print the number of records allocate to each user
    show_users_allocation(record_pd, user, selected)
    input('\nPress any key to start...')
    # Make selection interactively
    cur_time = datetime.now().strftime("%Y%m%d%H%M%S")
    select_records(record_pd, user, labels, selected, progress, cur_time)
    # write the selection
    output_fp = get_output_fp(args, user, cur_time[:8])
    write_selection(output_fp, record_pd, selected)
