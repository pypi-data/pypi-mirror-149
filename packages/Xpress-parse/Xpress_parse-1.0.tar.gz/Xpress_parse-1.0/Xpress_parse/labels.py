# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
from os.path import isfile


def curate_labels(labels: dict) -> None:
    """Removed keyword from the labels that are reserved to leave the parsing.

    Parameters
    ----------
    labels : dict
        Mapping from keywords (keys) to labels (values)
    """
    if 'exit' in labels:
        print('Removing "exit" form labels (reserved to exit...)')
        del labels['exit']
    if 'quit' in labels:
        print('Removing "quit" form labels (reserved to exit...)')
        del labels['quit']
    if 'stop' in labels:
        print('Removing "quit" form labels (reserved to exit...)')
        del labels['stop']


def get_labels(args: dict) -> dict:
    """Get the labels from file or from user interactively.

    Parameters
    ----------
    args : dict
        All arguments, including:
            labels_fp : str
                Path to file with 2 tab-separated columns: keywords and labels

    Returns
    -------
    labels : dict
        Mapping from keywords (keys) to labels (values)
    """
    labels_fp = args['labels_fp']
    if labels_fp and isfile(labels_fp):
        labels = read_labels(labels_fp)
    else:
        labels = collect_labels()
    curate_labels(labels)
    return labels


def read_labels(labels_fp: str) -> dict:
    """Read labels from file.

    Parameters
    ----------
    labels_fp : str
        Path to file with 2 tab-separated columns: keywords and labels

    Returns
    -------
    labels : dict
        Mapping from keywords (keys) to labels (values)
    """
    labels_pd = pd.read_csv(labels_fp, header=None, sep='\t', usecols=[0, 1])
    labels = dict(labels_pd.values)
    return labels


def collect_labels() -> dict:
    """Get the labels from user interactively.

    Returns
    -------
    labels : dict
        Mapping from keywords (keys) to labels (values)
    """
    ret, paired, v = '', 0, []
    print('\n%s\nDefine keywords to label studies?\n%s' % ('-'*33, '-'*33))
    while 1:
        if paired % 2 == 0:
            key_label = '[<ENTER> to stop] keyword: '
        else:
            key_label = '> label for "%s": ' % v[-1]
        ret = input(key_label)
        if not ret:
            break
        v.append(ret)
        paired += 1
    labels = dict((y, v[x + 1]) for x, y in enumerate(v[:-1]) if x % 2 == 0)
    return labels
