#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
from wer import wer
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.stats import percentileofscore


def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate metrics from two ctms, first one gold standard')
    parser.add_argument('gold', type=str,
                        help='The gold standard ctm, which to compare to')
    parser.add_argument('created', type=str,
                        help='The created ctm, which are evaluated')
    parser.add_argument('name', type=str,
                        help='Root name for the generated files')
    args = parser.parse_args()
    return args


# Read the ctms to a dataframe
def create_ctm_dfs(gold_ctms_file, created_ctms_file):
    column_names = ["Filename", "segment", "start", "duration", "token"]

    gold_ctms_df = pd.read_csv(gold_ctms_file, sep=' ', names=column_names, index_col=False, engine='python')
    created_ctms_df = pd.read_csv(created_ctms_file, sep=' ', names=column_names, index_col=False, engine='python')

    # Create end-time column
    '''df['c'] = df.apply(lambda row: row.a + row.b, axis=1)
    If you get the SettingWithCopyWarning you can do it this way also:

    fn = lambda row: row.a + row.b # define a function for the new column
    col = df.apply(fn, axis=1) # get column data with an index
    df = df.assign(c=col.values) # assign values to column 'c'
    '''
    gold_ctms_df["end"] = gold_ctms_df.apply(lambda row: row.start + row.duration, axis=1)
    created_ctms_df["end"] = created_ctms_df.apply(lambda row: row.start + row.duration, axis=1)

    return gold_ctms_df, created_ctms_df


def calculate_frame_wise_comparison(gold_ctms_df, created_ctms_df):
    fast_total_correct_empty_frames = []
    fast_total_correct_token_frames = []
    fast_total_incorrect_token_frames = []

    # Iterate file by file
    list_of_filenames = gold_ctms_df["Filename"].unique().tolist()

    # Create dataframe with index every framerate (10ms) and initialize with silence
    for filename in list_of_filenames:
        correct_empty_frames = 0
        correct_token_frames = 0
        incorrect_token_frames = 0

        df_current_gold_ctm = gold_ctms_df.loc[gold_ctms_df['Filename'] == filename][["start", "end", "token"]]
        df_current_created_ctm = created_ctms_df.loc[created_ctms_df['Filename'] == filename][["start", "end", "token"]]

        endtime = int(max(df_current_gold_ctm["end"].max(), df_current_created_ctm["end"].max()) * 1000)  # in ms
        framerate = 10  # in ms
        frames_current_gold_ctm = ["!SIL" for x in range(0, endtime + framerate, framerate)]
        frames_current_created_ctm = ["!SIL" for x in range(0, endtime + framerate, framerate)]

        # Go over the ctm token by token and use times to put that token into those indexes
        for frames_and_ctm in [[df_current_gold_ctm, frames_current_gold_ctm],
                               [df_current_created_ctm, frames_current_created_ctm]]:
            for ctm_row in frames_and_ctm[0].itertuples():

                # Calculate the indexes with framerate
                tokens_start_index = int(ctm_row.start * 1000 / framerate)
                tokens_end_index = int(ctm_row.end * 1000 / framerate)
                for index in range(tokens_start_index, tokens_end_index + 1):
                    frames_and_ctm[1][index] = ctm_row.token

        for gold_frame, created_frame in zip(frames_current_gold_ctm, frames_current_created_ctm):
            if gold_frame == "!SIL" and created_frame == "!SIL":
                correct_empty_frames += 1
            elif gold_frame == created_frame:
                correct_token_frames += 1
            else:
                incorrect_token_frames += 1

        fast_total_correct_token_frames.append(correct_token_frames)
        fast_total_correct_empty_frames.append(correct_empty_frames)
        fast_total_incorrect_token_frames.append(incorrect_token_frames)

    return [fast_total_correct_token_frames, fast_total_correct_empty_frames, fast_total_incorrect_token_frames]


def calculate_ctm_mistakes(gold_ctms_df, created_ctms_df):
    ctm_mistakes_seconds = []
    list_of_filenames = gold_ctms_df["Filename"].unique().tolist()
    for filename in list_of_filenames:

        df_current_gold_ctm = gold_ctms_df.loc[gold_ctms_df['Filename'] == filename][["start", "end", "token"]]
        df_current_created_ctm = created_ctms_df.loc[created_ctms_df['Filename'] == filename][["start", "end", "token"]]

        # ["OP", "REF", "HYP"]
        # "OK","SUB","INS", "***", "DEL", "***"
        wer_results, token_comparisons = \
            wer(df_current_gold_ctm["token"].tolist(), df_current_created_ctm["token"].tolist(), True)

        # Iterate three things
        gold_iterator = df_current_gold_ctm.itertuples()
        created_iterator = df_current_created_ctm.itertuples()
        for comparison_row in token_comparisons[1:]:
            if comparison_row[0] == "OK" or comparison_row[0] == "SUB":

                gold_ctm_row = next(gold_iterator)
                created_ctm_row = next(created_iterator)

                start_difference = created_ctm_row.start - gold_ctm_row.start
                end_difference = created_ctm_row.end - gold_ctm_row.end
                ctm_mistakes_seconds.append([start_difference, end_difference])

            elif comparison_row[0] == "INS":
                created_ctm_row = next(created_iterator)
            elif comparison_row[0] == "DEL":
                gold_ctm_row = next(gold_iterator)
            else:
                print("Something went terribly wrong")
                break
    return ctm_mistakes_seconds


def draw_histogram(data, xlabel, ylabel, title, xlim, name_of_histogram):
    plt.hist(data, 100, facecolor='g', alpha=0.75)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(-xlim, xlim)
    plt.grid(True)
    plt.savefig(name_of_histogram, bbox_inches='tight')


def draw_whiskers_plot(frame_wise_data, name_of_whiskers_plot):
    fig1, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
    ax1.set_title('Token')
    ax2.set_title('Empty')
    ax3.set_title('Wrong')
    ax1.boxplot(frame_wise_data[0])
    ax2.boxplot(frame_wise_data[1])
    ax3.boxplot(frame_wise_data[2])
    plt.savefig(name_of_whiskers_plot, bbox_inches='tight')
    plt.clf()


def calculate_statistics(ctm_mistakes_seconds):
    # Median start difference
    start_difference_median = np.median(ctm_mistakes_seconds[:, 0])

    list_of_percentileofscores = []
    # What percentage of tokens are inside 10ms, 25ms, 50ms, 100ms of actual start
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 0]), 0.01))
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 0]), 0.025))
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 0]), 0.05))
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 0]), 0.1))

    # What percentage of tokens are inside 10ms, 25ms, 50ms, 100ms of actual end
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 1]), 0.01))
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 1]), 0.025))
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 1]), 0.05))
    list_of_percentileofscores.append(percentileofscore(np.abs(ctm_mistakes_seconds[:, 1]), 0.1))

    return start_difference_median, list_of_percentileofscores


def main(gold_ctms_file, created_ctms_file, name):
    gold_ctm_df, created_ctm_df = create_ctm_dfs(gold_ctms_file, created_ctms_file)
    frame_wise_comparisons = calculate_frame_wise_comparison(gold_ctm_df, created_ctm_df)
    ctm_mistakes_seconds = calculate_ctm_mistakes(gold_ctm_df, created_ctm_df)

    name_of_whiskers_plot = name + "_whiskers_plot.png"
    draw_whiskers_plot(frame_wise_comparisons, name_of_whiskers_plot)

    nparray_ctm_mistakes_seconds = np.asarray(ctm_mistakes_seconds)
    name_of_histogram_start = name + "_histogram_start.png"
    draw_histogram(nparray_ctm_mistakes_seconds[:, 0], "Start difference", "# tokens", "Histogram of start differences", 0.03, name_of_histogram_start)

    name_of_histogram_end = name + "_histogram_end.png"
    draw_histogram(nparray_ctm_mistakes_seconds[:, 1], "End difference", "# tokens", "Histogram of end differences", 0.03, name_of_histogram_end)

    statistics = calculate_statistics(nparray_ctm_mistakes_seconds)
    print(statistics)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.gold, arguments.created, arguments.name)
