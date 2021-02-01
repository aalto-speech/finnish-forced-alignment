#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import pympi
import pathlib
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description='Write TextGrid file into ctm')
    parser.add_argument('name', type=str,
                        help='Path/Name of the TextGrid file')
    args = parser.parse_args()
    return args


def clean_text(text):
    text = re.sub(r'\([^)]*\)', '', text)
    text = text.lower()
    text = re.sub(r"[^\w ']", " ", text, flags=re.UNICODE)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text


def create_ctm_from_textgrid(textgrid_file):
    textgrid_path = pathlib.Path(textgrid_file)
    textgrid = pympi.Praat.TextGrid(textgrid_path, codec='8859')
    textgrid_id = textgrid_path.stem
    textgrid_parent_dir = textgrid_path.parents

    ctm_name = pathlib.Path(textgrid_parent_dir[1], "CTM", textgrid_id).with_suffix(".ctm")
    text_name = pathlib.Path(textgrid_parent_dir[1], "TXT", textgrid_id).with_suffix('.txt')

    with open(text_name, "w", encoding="utf-8") as text_file, \
            open(ctm_name, "w", encoding="utf-8") as ctm_file:
        for tier in textgrid.tiers:
            if tier.name == "sentence":
                interval_strings = []
                for interval in tier.intervals:
                    interval_strings.append(interval[2])
                utterance_text = clean_text(" ".join(interval_strings))
                text_file.write(textgrid_id + " " + utterance_text + "\n")
            elif tier.name == "word":
                for word in tier.intervals:
                    if len(word[2]) > 0:
                        word_string = " ".join([str(word[0]), str(word[1] - word[0]), clean_text(word[2])])
                        ctm_line = textgrid_id + " 1 " + word_string + "\n"
                        ctm_file.write(ctm_line)
            elif tier.name == "phone":
                continue
            else:
                print("Something odd happened")


def main(textgrid_file):
    create_ctm_from_textgrid(textgrid_file)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.name)
