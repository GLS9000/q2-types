# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd

import qiime2

from ..plugin_setup import plugin
from . import AlphaDiversityFormat


def _read_alpha_diversity(fh):
    # Using `dtype=object` and `set_index` to avoid type casting/inference
    # of any columns or the index.
    df = pd.read_csv(fh, sep='\t', header=0, dtype=object)
    df.set_index(df.columns[0], drop=True, append=False, inplace=True)
    df.index.name = None
    return df


@plugin.register_transformer
def _1(data: pd.Series) -> AlphaDiversityFormat:
    ff = AlphaDiversityFormat()
    with ff.open() as fh:
        data.to_csv(fh, sep='\t', header=True)
    return ff


@plugin.register_transformer
def _2(ff: AlphaDiversityFormat) -> pd.Series:
    with ff.open() as fh:
        df = _read_alpha_diversity(fh)
        return pd.to_numeric(df.iloc[:, 0])


@plugin.register_transformer
def _3(ff: AlphaDiversityFormat) -> qiime2.Metadata:
    with ff.open() as fh:
        return qiime2.Metadata(_read_alpha_diversity(fh))
