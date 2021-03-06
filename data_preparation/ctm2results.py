#!/usr/bin/env python
# coding: utf-8

# Imports
import pandas as pd
import argparse
import pathlib
import pympi


def parse_arguments():
    parser = argparse.ArgumentParser(description='Create textgrid and eaf files from Kaldi ctm')
    parser.add_argument('ctm_file', type=str,
                        help='The ctm from which to create the eaf and textgrid')
    args = parser.parse_args()
    return args


def create_ctm_df(ctm_file):
    column_names = ["Filename", "segment", "start", "duration", "token"]

    ctm_df = pd.read_csv(ctm_file, sep=' ', names=column_names, index_col=False, engine='python', encoding='utf-8')

    ctm_df["end"] = ctm_df.apply(lambda row: round(row.start + row.duration, 4), axis=1)

    return ctm_df


def create_elan_textgrid(ctm_df, target_directory):
    list_of_filenames = ctm_df["Filename"].unique().tolist()
    for filename in list_of_filenames:
        df_current_ctm = ctm_df.loc[ctm_df['Filename'] == filename][["start", "end", "token"]]

        textgrid_path = pathlib.Path(target_directory, str(filename)).with_suffix(".TextGrid")
        eaf_path = pathlib.Path(target_directory, str(filename)).with_suffix(".eaf")
        ctm_path = pathlib.Path(target_directory, str(filename)).with_suffix(".ctm")

        max_time = df_current_ctm["end"].max()
        textgrid = pympi.Praat.TextGrid(xmax=max_time, codec='utf-8')
        word_tier = textgrid.add_tier(name="words")
        for ctm_row in df_current_ctm.itertuples():
            word_tier.add_interval(ctm_row.start, ctm_row.end, ctm_row.token)

        textgrid.to_file(str(textgrid_path), codec='utf-8')
        eaf = textgrid.to_eaf()
        eaf.to_file(str(eaf_path))
        df_current_ctm.to_csv(str(ctm_path), index=False, header=None, sep=' ')


def main(ctm_file):
    ctm_df = create_ctm_df(ctm_file)
    ctm_directory = pathlib.Path(ctm_file).parent
    create_elan_textgrid(ctm_df, str(ctm_directory))


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.ctm_file)
