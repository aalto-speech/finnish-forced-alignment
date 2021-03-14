#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import os
import sys
import wave
import subprocess


def parse_arguments():
    parser = argparse.ArgumentParser(description='Write individual .txt files from kaldi text file')
    parser.add_argument('targetdir', type=str,
                        help='Path/Name of the target directory where it is ok to create files')
    parser.add_argument('--datadir', type=str,
                        help='Path/Name of the data directory')
    parser.add_argument('--wav', type=str,
                        help='Path/Name of the audio file or directory')
    parser.add_argument('--txt', type=str,
                        help='Path/Name of the text file or directory')
    parser.add_argument('--ctm', type=str,
                        help='Path/Name of the created ctm file')
    parser.add_argument('--eaf', type=str,
                        help='Path/Name of the created eaf file')
    parser.add_argument('--textgrid', type=str,
                        help='Path/Name of the textgrid file')
    parser.add_argument('--lang', type=str, default='fi', choices=('fi', 'en', 'se'),
                        help='Target language')
    args = parser.parse_args()

    if args.datadir is None and (args.wav is None or args.txt is None):
        parser.error('Please provide either the data directory or wav and txt directories (or individual files).')
    if args.targetdir == "align":
        parser.error('Please give another name than align for target directory')

    return args


def check_framerate(wavpath):
    prompt_text = """
    You have an audio file with framerate incompatible with Kaldi ASR. As most speech recognizers 
    Kaldi uses 16000Hz wav files. If you want to continue Kaldi can downsample, but we cannot guarantee the results.
    If you want to change the rate yourself press any key, TO CONTINUE PRESS y"""
    listofwavs = []
    one_wrong_type = False
    if os.path.isdir(wavpath):
        listofwavs = sorted(os.listdir(wavpath))
    elif os.path.isfile(wavpath):
        listofwavs.append(os.path.split(wavpath)[1])
        wavpath = os.path.split(wavpath)[0]

    for wavname in listofwavs:
        _, file_extension = os.path.splitext(wavname)
        if file_extension == ".wav":
            with wave.open(os.path.join(wavpath, wavname), "rb") as wave_file:
                frame_rate = wave_file.getframerate()
                if frame_rate != 16000:
                    one_wrong_type = True
    if one_wrong_type:
        if input(prompt_text) != "y":
            sys.exit()


def main(arguments):
    csv_file = "phone-finnish-finnish.csv"
    if arguments.lang == 'en':
        csv_file = "phone-english-finnish.csv"
    elif arguments.lang == 'se':
        csv_file = "phone-sami-finnish.csv"
    if arguments.datadir:
        check_framerate(arguments.datadir)
        rc = subprocess.call(["/tmp/matthies/align.sh", csv_file, arguments.targetdir, arguments.datadir])
    elif arguments.wav:
        check_framerate(arguments.wav)
        rc = subprocess.call(["/tmp/matthies/align.sh", csv_file, arguments.targetdir, arguments.wav, arguments.txt])


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
