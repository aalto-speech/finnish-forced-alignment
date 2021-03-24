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
    parser.add_argument('--lang', type=str, default='fi', choices=('fi', 'en', 'se', 'et'),
                        help='Target language')
    parser.add_argument('--debug', action='store_true',
                        help='Run script in debug mode meaning certain files are not deleted afterwards')
    args = parser.parse_args()

    if args.datadir is None and (args.wav is None or args.txt is None):
        parser.error('Please provide either the data directory or wav and txt directories (or individual files).')
    if {"align", "kohdistus", "src_for_wav", "src_for_txt"} & {args.targetdir, args.datadir, args.wav, args.txt}:
        parser.error('Please give another name than align, kohdistus, src_for_wav or src_for_txt for directories')

    return args


def collect_files_in_dir(path, file_extension):
    list_of_files = []
    list_of_correct_files = []
    path_to_files = ""
    if os.path.isdir(path):
        list_of_files = sorted(os.listdir(path))
        path_to_files = path
    elif os.path.isfile(path):
        list_of_files.append(os.path.split(path)[1])
        path_to_files = os.path.split(path)[0]

    for name in list_of_files:
        _, current_file_extension = os.path.splitext(name)
        if current_file_extension == file_extension:
            list_of_correct_files.append([name, os.path.join(path_to_files, name)])

    return list_of_correct_files


def check_framerate(wavpath):
    prompt_text = """
    You have an audio file with framerate incompatible with Kaldi ASR. As most speech recognizers 
    Kaldi uses 16000Hz wav files. If you want to continue Kaldi can downsample, but we cannot guarantee the results.
    If you want to change the rate yourself press any key, TO CONTINUE PRESS y and [ENTER]: """
    list_of_wavs = collect_files_in_dir(wavpath, ".wav")
    one_wrong_type = False

    for wav in list_of_wavs:
        with wave.open((wav[1]), "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            if frame_rate != 16000:
                one_wrong_type = True
    if one_wrong_type:
        if input(prompt_text) != "y":
            sys.exit()


def check_files(wavpath, txtpath):
    prompt_text = """
    If you want to fix the situation before continuing press any key, TO CONTINUE PRESS y and [ENTER]: """

    list_of_wavs = collect_files_in_dir(wavpath, ".wav")
    list_of_txts = collect_files_in_dir(txtpath, ".txt")
    list_of_names_in_wav = [x[1] for x in list_of_wavs]
    list_of_names_in_txt = [x[1] for x in list_of_txts]

    if len(list_of_names_in_wav) != len(list_of_names_in_txt):
        print("number of wav files is {}, txt files {}".format(len(list_of_names_in_wav), len(list_of_names_in_txt)))
        print("There is a different amount of files")
        print("The following txt files are not in wav files")
        print(set(list_of_names_in_txt) - set(list_of_names_in_wav))
        print("The following wav files are not in txt files")
        print(set(list_of_names_in_wav) - set(list_of_names_in_txt))
        if input(prompt_text) != "y":
            sys.exit()


def main(arguments):
    csv_file = "phone-finnish-finnish.csv"
    if arguments.lang == 'en':
        csv_file = "phone-english-finnish.csv"
    elif arguments.lang == 'se':
        csv_file = "phone-sami-finnish.csv"
    elif arguments.lang == 'et':
        csv_file = "phone-estonian-finnish.csv"
    debug = "false"
    if arguments.debug:
        debug = "true"
    if arguments.datadir:
        check_framerate(arguments.datadir)
        check_files(arguments.datadir, arguments.datadir)
        rc = subprocess.call(
            ["/tmp/matthies/align.sh",
             csv_file,
             debug,
             arguments.targetdir,
             arguments.datadir])

    elif arguments.wav:
        check_framerate(arguments.wav)
        check_files(arguments.wav, arguments.txt)
        rc = subprocess.call(
            ["/tmp/matthies/align.sh",
             csv_file,
             debug,
             arguments.targetdir,
             arguments.wav,
             arguments.txt])


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
