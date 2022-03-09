#!/usr/bin/env python3

import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Makes files kaldi needs for alignment.')
    parser.add_argument('wavpath', type=str,
                        help='The path to the wav.scp.')
    parser.add_argument('recopath', type=str,
                        help='The path to the reco2channel_and_file.')
    args = parser.parse_args()
    return args


def make_reco(wavpath, recopath):
    with open(wavpath, "r", encoding="utf-8") as wavlist_file,\
        open(recopath, "w", encoding="utf-8") as reco_file:

        for wav in wavlist_file:
            recording_id, recording_path = wav.split(" ")
            filename = os.path.splitext(os.path.split(recording_path)[1])[0]
            reco_file.write(recording_id + " " + filename + " 1\n")


def main(arguments):
    make_wav(arguments.wavpath, arguments.tgtpath)
    if arguments.txtpath:
        make_txt(arguments.txtpath, arguments.tgtpath)
    else:
        make_txt(arguments.wavpath, arguments.tgtpath)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
