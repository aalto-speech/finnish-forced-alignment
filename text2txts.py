#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description='Write individual .txt files from kaldi text file')
    parser.add_argument('name', type=str,
                        help='Path/Name of the text file')
    args = parser.parse_args()
    return args


def create_txts_from_text(text_file):
    with open(text_file, "r", encoding="utf-8") as text:
        for line in text:
            line = line.strip()
            line_parts = line.split(" ")
            utterance_ID = line_parts[0]
            utterance_text = " ".join(line_parts[1:]) + "\n"
            with open(utterance_ID + ".txt", "w", encoding="utf-8") as utterance_file:
                utterance_file.write(utterance_text)


def main(text_file):
    create_txts_from_text(text_file)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.name)
