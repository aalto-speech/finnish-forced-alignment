#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Change ctm end column to duration column to fit analysis pipeline')
    parser.add_argument('ctm_end', type=str,
                        help='The end column ctm')
    parser.add_argument('ctm_dur', type=str,
                        help='The new duration column ctm')
    args = parser.parse_args()
    return args


def create_ctm_df(ctm_file):
    column_names = ["Filename", "segment", "start", "end", "token"]

    ctm_df = pd.read_csv(ctm_file, sep=' ', names=column_names, index_col=False, engine='python', encoding='utf-8')

    ctm_df["duration"] = ctm_df.apply(lambda row: round(row.end - row.start, 4), axis=1)

    return ctm_df


def main(ctm_end, ctm_dur):
    ctm_df = create_ctm_df(ctm_end)
    ctm_df[["Filename", "segment", "start", "duration", "token"]].to_csv(ctm_dur, index=False, header=None, sep=' ')


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.ctm_end, arguments.ctm_dur)
