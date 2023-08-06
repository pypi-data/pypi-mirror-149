# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import json
import glob
import hashlib
from os.path import dirname, isdir


def get_progress_files(
        progress: str,
        selected: dict) -> None:
    """Fill the selected object with the latest records selection.

    Parameters
    ----------
    args : dict
        All arguments, including:
            input_fps : tuple
                Path(s) to WoS search result(s)
    progress : str
        Path to the file (no extension) that will contain the progress
        for the currently parsed WoS searches
    selected : dict
        Selected records
    """
    to_glob = '%s_2*.tsv' % progress
    fps = sorted(glob.glob(to_glob))
    if len(fps):
        file_handle = open(fps[-1], "r")
        selected.update(json.load(file_handle))
        file_handle.close()


def get_progress_base(args: dict) -> str:
    """Get the folder and basename where the progress data will be kept updated.

    Parameters
    ----------
    args : dict
        All arguments, including:
            input_fps : tuple
                Path(s) to WoS search result(s)

    Returns
    -------
    progress : str
        Path to the file (no extension) that will contain the progress
        for the currently parsed WoS searches
    """
    input_fps = args['input_fps']
    folder = '%s/.xpress' % dirname(input_fps[0])
    base = hashlib.sha224(''.join(input_fps).encode()).hexdigest()
    progress = folder + '/' + base
    return progress


def read_past_progress(args: dict) -> tuple:
    """Initialization checks whether the output file already exists which
    means you already made selection and stopped.

    Parameters
    ----------
    args : dict
        All arguments, including:
            input_fps : tuple
                Path(s) to WoS search result(s)

    Returns
    -------
    selected : dict
        Selected records
    progress : str
        Path to the file (no extension) that will contain the progress
        for the currently parsed WoS searches
    """
    progress = get_progress_base(args)
    selected = {}
    if isdir(dirname(progress)):
        get_progress_files(progress, selected)
    return selected, progress
