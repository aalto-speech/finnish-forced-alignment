#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description='Write individual .txt files from kaldi text file')
    parser.add_argument('text_file', type=str,
                        help='Path/Name of the text file')
    parser.add_argument('--parent_dir', type=str,
                        help='Path/name to the directory with new txts')
    args = parser.parse_args()
    return args


def create_txts_from_text(text_file, directory=None):
    text_path = pathlib.Path(text_file)
    text_parent_dir = text_path.parents
    if directory == None:
        target_directory = text_parent_dir[1]
    else:
        target_directory = directory

    with open(text_file, "r", encoding="utf-8") as text:
        for line in text:
            line = line.strip()
            line_parts = line.split(" ")
            utterance_ID = line_parts[0]
            utterance_text = " ".join(line_parts[1:]) + "\n"
            utterance_name = pathlib.Path(utterance_ID).with_suffix(".txt")
            with open(utterance_name, "w", encoding="utf-8") as utterance_file:
                utterance_file.write(utterance_text)


def main(arguments):
    create_txts_from_text(arguments.text_file, arguments.parent_dir)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
