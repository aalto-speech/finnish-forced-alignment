#!/usr/bin/env python
# coding: utf-8

# Imports
import sys
import copy
import pandas
import argparse
from analysis.calculate_metrics import create_ctm_dfs  # breaks if run as a script and not -m


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


def split_silence(created_df, split_type, pause_duration):
    splitted_df = copy.deepcopy(created_df)

    start_list_ms = (splitted_df["start"] * 1000).map(int).tolist()
    duration_list_ms = (splitted_df["duration"] * 1000).map(int).tolist()
    end_list_ms = (splitted_df["end"] * 1000).map(int).tolist()
    pause_duration_ms = int(pause_duration * 1000)

    for i in range(len(start_list_ms) - 1):
        pause = start_list_ms[i + 1] - end_list_ms[i]
        if 0 < pause < pause_duration_ms:
            # Kaldi resolution is 10ms so pause should always be divisible by two
            if split_type == "middle":
                end_list_ms[i] += pause // 2
                duration_list_ms[i] += pause // 2
                duration_list_ms[i + 1] += pause // 2
                start_list_ms[i + 1] -= pause // 2
            elif split_type == "end":
                end_list_ms[i] += pause
                duration_list_ms[i] += pause
            elif split_type == "start":
                start_list_ms[i + 1] -= pause
                duration_list_ms[i + 1] += pause
            else:
                sys.exit("Error, no split type. Should not be possible to reach this point.")
        else:
            continue  # To spell out the algorithm

    splitted_df["start"] = [float(i) / 1000 for i in start_list_ms]
    splitted_df["duration"] = [float(i) / 1000 for i in duration_list_ms]
    splitted_df["end"] = [float(i) / 1000 for i in end_list_ms]

    return splitted_df


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
