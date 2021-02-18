#!/usr/bin/env python3

import os
import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Makes files kaldi needs for alignment.')
    parser.add_argument('srcpath', type=str,
                        help='The path to the wav files.')
    parser.add_argument('targetpath', type=str,
                        help='The path to write kaldi files.')
    args = parser.parse_args()
    return args

def make_kaldi_files(srcpath, targetpath):
    wav_name = os.path.join(targetpath, "data/align/wav.scp")
    utt2spk_name = os.path.join(targetpath, "data/align/utt2spk")

    with open(wav_name, "w", encoding="utf-8") as wavlist_file,\
        open(utt2spk_name, "w", encoding="utf-8") as utt2spk_file:

        for dirfile in sorted(os.listdir(srcpath)):
            filename, file_extension = os.path.splitext(dirfile)
            if file_extension == ".wav":
                wavlist_file.write(filename + " " + os.path.join(srcpath, dirfile) + "\n")

                utt2spk_file.write(filename + " " + filename + "\n")

def main(srcpath, targetpath):
    make_kaldi_files(srcpath, targetpath)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.srcpath, arguments.targetpath)
