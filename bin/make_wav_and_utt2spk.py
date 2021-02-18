#!/usr/bin/env python3

import os
import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Makes files kaldi needs for alignment.')
    parser.add_argument('basepath', type=str,
                        help='The path to the wav files.')
    args = parser.parse_args()
    return args

def make_kaldi_files(basepath):
    wav_name = "data/align/wav.scp"
    utt2spk_name = "data/align/utt2spk"

    with open(wav_name, "w", encoding="utf-8") as wavlist_file,\
        open(utt2spk_name, "w", encoding="utf-8") as utt2spk_file:

        for dirfile in sorted(os.listdir(basepath)):
            filename, file_extension = os.path.splitext(dirfile)
            if file_extension == ".wav":
                wavlist_file.write(filename + " " + os.path.join(basepath, dirfile) + "\n")

                utt2spk_file.write(filename + " " + filename + "\n")

def main(basepath):
    make_kaldi_files(basepath)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.basepath)
