#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
import argparse
import os
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description='Write Elan produced tab aligned files into Kaldi ctms')
    parser.add_argument('name', type=str,
                        help='Path/Name of the tab file')
    parser.add_argument('--re', action='store_true',
                        help='Whether to apply regular expressions on word tokens')
    args = parser.parse_args()
    return args


# Read the tab aligned file to a dataframe
def create_ctm_and_text(tab_aligned_file, apply_re):
    column_names = ["type", "speaker", "start", "end", "duration", "token"]

    tab_aligned_df = pd.read_csv(tab_aligned_file, sep='\t', names=column_names, index_col=False, engine='python')
    filename = os.path.basename(tab_aligned_file)
    filename = filename.split('.')[0]
    dirname = os.path.dirname(tab_aligned_file)

    filename_column = [filename] * tab_aligned_df.shape[0]
    segment_column = ["A"] * tab_aligned_df.shape[0]
    tab_aligned_df["filename"] = filename_column
    tab_aligned_df["segment"] = segment_column

    ctm_df = tab_aligned_df[["filename", "segment", "start", "duration", "token"]]
    ctm_df = ctm_df.sort_values(by=["start"])

    ctm_df["token"] = ctm_df["token"].fillna("2'34'45'78'2")
    if apply_re:
        ctm_df["token"] = [re.sub(r'\([^)]*\)', '', str(x)) for x in ctm_df["token"]]
        ctm_df["token"] = ctm_df["token"].str.lower()
        ctm_df["token"] = [re.sub(r"[^\w ']", "", str(x), flags=re.UNICODE) for x in ctm_df["token"]]
        ctm_df["token"] = [re.sub(' +', ' ', str(x)) for x in ctm_df["token"]]
        ctm_df["token"] = ctm_df["token"].str.strip()
    ctm_df["token"] = ctm_df["token"].str.replace("2'34'45'78'2", '<UNK>')
    ctm_save_name = os.path.join(dirname, (filename + ".csv"))
    ctm_df.to_csv(ctm_save_name, index=False, header=None, sep=' ')

    tokens_as_list = ctm_df["token"].tolist()
    tokens_as_string = filename + " " + " ".join(tokens_as_list) + "\n"

    textfile_save_name = os.path.join(dirname, (filename + ".txt"))
    with open(textfile_save_name, "w", encoding="utf-8") as textfile:
        textfile.write(tokens_as_string)


def main(tab_aligned_file, apply_re):
    create_ctm_and_text(tab_aligned_file, apply_re)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.name, arguments.re)
