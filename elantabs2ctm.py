#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
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
    column_names = ["type", "speaker", "start", "end", "duration", "token"]

    tab_aligned_df = pd.read_csv(tab_aligned_file, sep='\t', names=column_names, index_col=False, engine='python')
    filename = os.path.basename(tab_aligned_file)
    filename = filename.split('.')[0]
    dirname = os.path.dirname(tab_aligned_file)

    filename_column = [filename] * tab_aligned_df.shape[0]
    segment_column = ["1"] * tab_aligned_df.shape[0]
    tab_aligned_df["filename"] = filename_column
    tab_aligned_df["segment"] = segment_column

    ctm_df = tab_aligned_df[["filename", "segment", "start", "end", "token"]]
    ctm_df = ctm_df.sort_values(by=["start"])
    ctm_save_name = os.path.join(dirname, (filename + ".csv"))
    ctm_df.to_csv(ctm_save_name, index=False, sep=' ')

    tokens_as_list = ctm_df["token"].tolist()
    tokens_as_string = filename + " " + " ".join(tokens_as_list) + "\n"

    textfile_save_name = os.path.join(dirname, (filename + ".txt"))
    with open(textfile_save_name, "w", encoding="utf-8") as textfile:
        textfile.write(tokens_as_string)


def main(tab_aligned_file):
    create_ctm_and_text(tab_aligned_file)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.name)
