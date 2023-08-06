# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click

from Xpress_parse.xpress import xpress
from Xpress_parse import __version__


@click.command()
@click.option(
    "-i", "--i-records", multiple=True, help="Path(s) to WoS search result(s)")
@click.option(
    "-o", "--o-output", default=None, type=str,
    help="Selected records (default to xpress_records_YYYY-MM-DD.tsv)")
@click.option(
    "-u", "--p-user", multiple=True, default=None, help="User name(s)")
@click.option(
    "-l", "--p-labels", default=None,
    help="Path to file with 2 tab-separated columns: keywords and labels")
@click.version_option(__version__, prog_name="Xpress_parse")


def standalone_xpress(
        i_records,
        o_output,
        p_user,
        p_labels,
):

    xpress(
        input_fps=i_records,
        output_fp=o_output,
        user=p_user,
        labels_fp=p_labels,
    )


if __name__ == "__main__":
    standalone_xpress()
