#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import pympi
import pathlib
import re


def parse_arguments():
    parser = argparse.ArgumentParser(description='Write TextGrid file into ctm')
    parser.add_argument('textgrid', type=str,
                        help='Path/Name of the TextGrid file')
    parser.add_argument('--parent_dir', type=str,
                        help='Path/name to the directory with new txt and ctm directories')
    args = parser.parse_args()
    return args


def clean_text(text):
    text = re.sub(r'\([^)]*\)', '', text)
    text = text.lower()
    text = re.sub(r"[^\w ']", " ", text, flags=re.UNICODE)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text


def create_ctm_from_textgrid(textgrid_file, directory=None):
    textgrid_path = pathlib.Path(textgrid_file)
    textgrid = pympi.Praat.TextGrid(textgrid_path, codec='8859')
    textgrid_id = textgrid_path.stem
    textgrid_parent_dir = textgrid_path.parents
    if directory == None:
        target_directory = textgrid_parent_dir[1]
    else:
        target_directory = directory

    ctm_name = pathlib.Path(target_directory, "ctm", textgrid_id).with_suffix(".ctm")
    text_name = pathlib.Path(target_directory, "txt", textgrid_id).with_suffix('.txt')
    ctm_name.parent.mkdir(parents=True, exist_ok=True) # same behavior as the POSIX mkdir -p command
    text_name.parent.mkdir(parents=True, exist_ok=True) # same behavior as the POSIX mkdir -p command

    with open(text_name, "w", encoding="utf-8") as text_file, \
            open(ctm_name, "w", encoding="utf-8") as ctm_file:
        for tier in textgrid.tiers:
            if tier.name == "sentence":
                interval_strings = []
                for interval in tier.intervals:
                    interval_strings.append(interval[2])
                utterance_text = clean_text(" ".join(interval_strings))
                #text_file.write(textgrid_id + " " + utterance_text + "\n")
                text_file.write(utterance_text + "\n")
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


def main(arguments):
    create_ctm_from_textgrid(arguments.textgrid, arguments.parent_dir)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
