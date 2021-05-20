#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import os
import sys
import subprocess
from kaldi_rec_conf import container_name, singularity_wrapper

def parse_arguments():
    parser = argparse.ArgumentParser(description='Kaldi ASR')
    parser.add_argument('inputfile', type=str,
                        help='input, media filename (wav,mp4,avi,webm) or YouTube link')
    parser.add_argument('targetdir', type=str,
                        help='Path/Name of the target directory where it is ok to create files')
    parser.add_argument('--srt', action='store_true',
                        help='Insert this flag if you want srt file as an output')
    parser.add_argument('--eaf', action='store_true',
                        help='Insert this flag if you want eaf file as an output')
    parser.add_argument('--txt', action='store_true',
                        help='Insert this flag if you want txt file as an output')
    args = parser.parse_args()

    return args


def main(arguments):
    wav_path_for_container = "/opt/kaldi/egs/src_for_wav/"
    target_path_for_container = "/opt/kaldi/egs/temp/"

    input_directory, filename_with_extension = os.path.split(arguments.inputfile)
    filename, _ = os.path.splitext(filename_with_extension)
    abspath_inputdir = os.path.abspath(input_directory)
    abspath_targetdir = os.path.abspath(arguments.targetdir)

    bind_input = "-B  {}:{}".format(abspath_inputdir, wav_path_for_container)
    bind_output = ""
    output_file_pretext = wav_path_for_container
    if abspath_inputdir != abspath_targetdir:
        bind_output = "-B {}:{}".format(abspath_targetdir, target_path_for_container)
        output_file_pretext = target_path_for_container

    srt_text = ""
    txt_text = ""
    eaf_text = ""
    if arguments.srt:
        srt_text = "--srt " + output_file_pretext + filename + ".srt"
    if arguments.txt:
        txt_text = "--txt " + output_file_pretext + filename + ".txt"
    if arguments.eaf:
        eaf_text = "--eaf " + output_file_pretext + filename + ".eaf"

    inputfile = wav_path_for_container + filename_with_extension
    container_command = " ".join([bind_input, bind_output, container_name, inputfile, srt_text, txt_text, eaf_text])
    container_command = " ".join(container_command.split())  # Deletes extra whitespace
    print(container_command)

    rc = subprocess.call(
        [singularity_wrapper,
         container_command])


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
