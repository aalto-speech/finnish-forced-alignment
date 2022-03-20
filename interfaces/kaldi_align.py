#!/usr/bin/env python3
# coding: utf-8

# Imports
import argparse
import os
import sys
import wave
import subprocess
import yaml


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
    parser.add_argument('--segments', type=str,
                        help='Path/Name of the segments directory. WARNING! This option assumes you know what you are doing.')
    # parser.add_argument('--ctm', type=str,
    #                     help='Path/Name of the created ctm file')
    # parser.add_argument('--eaf', type=str,
    #                     help='Path/Name of the created eaf file')
    # parser.add_argument('--textgrid', type=str,
    #                     help='Path/Name of the textgrid file')
    parser.add_argument('--lang', type=str, default='fi', choices=('fi', 'fi-conv', 'en', 'se', 'et', 'kv'),
                        help='Target language')
    parser.add_argument('--container', type=str,
                        help='The Kaldi-align singularity container used for aligning speech.')
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
        name_without_extension, current_file_extension = os.path.splitext(name)
        if current_file_extension == file_extension:
            list_of_correct_files.append([name_without_extension, os.path.join(path_to_files, name)])

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
    list_of_names_in_wav = [x[0] for x in list_of_wavs]
    list_of_names_in_txt = [x[0] for x in list_of_txts]

    if len(list_of_names_in_wav) != len(list_of_names_in_txt):
        print("number of wav files is {}, txt files {}".format(len(list_of_names_in_wav), len(list_of_names_in_txt)))
        print("There is a different amount of files")
        print("The following txt files are not in wav files")
        print(set(list_of_names_in_txt) - set(list_of_names_in_wav))
        print("The following wav files are not in txt files")
        print(set(list_of_names_in_wav) - set(list_of_names_in_txt))
        if input(prompt_text) != "y":
            sys.exit()


def load_container_parameters(container_argument):
    interface_code_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(interface_code_directory, "config.yaml")
    with open(config_file_path) as config_file:
        # use safe_load instead load
        align_parameters = yaml.safe_load(config_file)
        container_name = align_parameters["align_container_name"]
        singularity_wrapper = align_parameters["singularity_wrapper"]

    if container_argument:  # isfile cannot handle None
        if os.path.isfile(container_argument):
            container_name = container_argument
        else:
            sys.exit("The path to container is not a file.")

    return container_name, singularity_wrapper


def main(arguments):

    container_name, singularity_wrapper = load_container_parameters(arguments.container)

    wav_path_for_container = "/opt/kaldi/egs/src_for_wav/"
    txt_path_for_container = "/opt/kaldi/egs/src_for_txt/"
    target_path_for_container = "/opt/kaldi/egs/kohdistus/"

    csv_file = "phone-finnish-finnish.csv"
    if arguments.lang == 'fi-conv':
        csv_file = "phone-converse-finnish.csv"
    elif arguments.lang == 'en':
        csv_file = "phone-english-finnish.csv"
    elif arguments.lang == 'se':
        csv_file = "phone-sami-finnish.csv"
    elif arguments.lang == 'et':
        csv_file = "phone-estonian-finnish.csv"
    elif arguments.lang == 'kv':
        csv_file = "phone-komi-finnish.csv"

    debug = "false"
    if arguments.debug:
        debug = "true"

    textDirBoolean = "textDirTrue"
    if arguments.datadir:
        wav_directory = arguments.datadir
        txt_directory = arguments.datadir
        check_framerate(wav_directory)
        check_files(wav_directory, txt_directory)
        textDirBoolean = "textDirFalse"
    elif arguments.segments:
        wav_directory = arguments.wav
        txt_directory = arguments.segments
        check_framerate(wav_directory)
        if os.path.isfile(arguments.wav):
            wav_directory, align_file_name = os.path.split(arguments.wav)
        textDirBoolean = "kaldiDirTrue"
    else:  # arguments.wav
        wav_directory = arguments.wav
        txt_directory = arguments.txt
        check_framerate(wav_directory)
        check_files(wav_directory, txt_directory)
        if os.path.isfile(arguments.wav):
            wav_directory, align_file_name = os.path.split(arguments.wav)
            txt_directory, _ = os.path.split(arguments.txt)

    abspath_input_wavdir = os.path.abspath(wav_directory)
    abspath_input_txtdir = os.path.abspath(txt_directory)
    abspath_targetdir = os.path.abspath(arguments.targetdir)

    bind_wav_input = "-B {}:{}".format(abspath_input_wavdir, wav_path_for_container)
    bind_txt_input = "-B {}:{}".format(abspath_input_txtdir, txt_path_for_container)
    bind_output = "-B {}:{}".format(abspath_targetdir, target_path_for_container)
    binding_string = " ".join([bind_wav_input, bind_txt_input, bind_output])

    if arguments.wav and os.path.isfile(arguments.wav):
        wav_path_for_container = wav_path_for_container + align_file_name
        txt_path_for_container = txt_path_for_container + align_file_name[:-3] + "txt"

    paths_for_container = wav_path_for_container + " " + txt_path_for_container

    container_command = " ".join([binding_string, container_name, csv_file, debug, textDirBoolean, paths_for_container])
    container_command = " ".join(container_command.split())
    print(container_command)

    rc = subprocess.call(
        [singularity_wrapper,
         container_command])


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
