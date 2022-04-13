#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
from finnish_forced_alignment.alignment import wer # breaks if run as a script and not -m
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.stats import percentileofscore

import finnish_forced_alignment.alignment as alignment


def main(gold_ctms_file, created_ctms_file, name):
    gold_ctm_df, created_ctm_df = alignment.create_ctm_dfs(gold_ctms_file, created_ctms_file)
    frame_wise_comparisons = alignment.calculate_frame_wise_comparison(gold_ctm_df, created_ctm_df)
    ctm_mistakes_seconds = alignment.calculate_ctm_mistakes(gold_ctm_df, created_ctm_df)

    name_of_whiskers_plot = name + "_whiskers_plot.png"
    alignment.draw_whiskers_plot(frame_wise_comparisons, name_of_whiskers_plot)

    nparray_ctm_mistakes_seconds = np.asarray(ctm_mistakes_seconds)
    name_of_histogram_start = name + "_histogram_start.png"
    alignment.draw_histogram(nparray_ctm_mistakes_seconds[:, 0], "Start difference", "# tokens", "Histogram of start differences", 0.5, name_of_histogram_start)

    name_of_histogram_end = name + "_histogram_end.png"
    alignment.draw_histogram(nparray_ctm_mistakes_seconds[:, 1], "End difference", "# tokens", "Histogram of end differences", 0.5, name_of_histogram_end)

    statistics = alignment.calculate_statistics(nparray_ctm_mistakes_seconds)
    print(statistics)

    if "sami" in arguments.name:
        alignment.calculate_time_from_ctms(gold_ctm_df, created_ctm_df)


if __name__ == '__main__':
    arguments = alignment.parse_arguments()
    main(arguments.gold, arguments.created, arguments.name)
