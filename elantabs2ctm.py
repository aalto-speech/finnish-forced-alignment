#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
import numpy as np
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description='Write Elan produced tab aligned files into Kaldi ctms')
    parser.add_argument('name', type=str,
                        help='Path/Name of the tab file')
    args = parser.parse_args()
    return args


# Read the tab aligned file to a dataframe
def create_ctm_and_text(tab_aligned_file):
    column_names = ["speaker1", "type", "speaker2", "start", "end", "duration", "token"]

    tab_aligned_df = pd.read_csv(tab_aligned_file, sep='\t', names=column_names, index_col=False, engine='python')
    filename = os.path.basename(os.path.splitext(tab_aligned_file)[0])

    filename_column = [filename] * tab_aligned_df.shape[0]
    segment_column = ["1"] * tab_aligned_df.shape[0]
    tab_aligned_df["filename"] = filename_column
    tab_aligned_df["segment"] = segment_column

    ctm_df = tab_aligned_df["filename", "segment", "start", "end", "token"]
    ctm_df.to_csv(filename + "_csv", index=False, sep=' ')

