import sys
import copy
import pandas
import argparse
from .alignment.calculate_metrics import create_ctm_dfs


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
