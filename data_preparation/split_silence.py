#!/usr/bin/env python
# coding: utf-8

# Imports
import sys
import copy
import pandas
import argparse
from analysis.calculate_metrics import create_ctm_dfs  # breaks if run as a script and not -m
from finnish_forced_alignment.data_handling.split_silence import split_silence

import finnish_forced_alignment
finnish_forced_alignment.data_handling.split_silence.split_silence()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate metrics from two ctms, first one gold standard')
    parser.add_argument('gold', type=str,
                        help='The gold standard ctm, which to compare to')
    parser.add_argument('created', type=str,
                        help='The created ctm, which are evaluated')
    parser.add_argument('splitted', type=str,
                        help='The location for the silence splitted ctm.')
    parser.add_argument('--split_type', type=str, default='none', choices=('middle', 'start', 'end', 'none'),
                        help='Will the silence be split in the middle, start or end')
    parser.add_argument('--pause_duration', type=float, default=0.5,
                        help='Max silence duration that will be split. After this considered between sentences.')
    args = parser.parse_args()
    return args



def main(gold_ctms_file, created_ctms_file, splitted_ctms_file, split_type, pause_duration):
    _, created_ctm_df = create_ctm_dfs(gold_ctms_file, created_ctms_file)
    if arguments.split_type == 'none':
        splitted_df = created_ctm_df
    else:
        splitted_df = split_silence(created_ctm_df, split_type, pause_duration)
    splitted_df[["Filename", "segment", "start", "duration", "token"]].to_csv(splitted_ctms_file, index=False,
                                                                                  header=None, sep=' ')


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.gold, arguments.created, arguments.splitted, arguments.split_type, arguments.pause_duration)
