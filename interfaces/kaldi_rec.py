#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import os
import sys
import subprocess
import yaml


def parse_arguments():
    parser = argparse.ArgumentParser(description='Kaldi ASR')
    parser.add_argument('inputfile', type=str,
                        help='input, media filename (wav)')
    parser.add_argument('targetdir', type=str,
                        help='Path/Name of the target directory where it is ok to create files')
    parser.add_argument('--srt', action='store_true',
                        help='Insert this flag if you want srt file as an output')
    parser.add_argument('--eaf', action='store_true',
                        help='Insert this flag if you want eaf file as an output')
    parser.add_argument('--txt', action='store_true',
                        help='Insert this flag if you want txt file as an output')
    parser.add_argument('--container', type=str,
                        help='The Kaldi-rec singularity container used for transcribing speech.')
    args = parser.parse_args()

    return args


#  Copy-pasted from kaldi_align.py but maybe better here than loaded from there?
def load_container_parameters(container_argument):
    interface_code_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(interface_code_directory, "config.yaml")
    with open(config_file_path) as config_file:
        # use safe_load instead load
        rec_parameters = yaml.safe_load(config_file)
        container_name = rec_parameters["rec_container_name"]
        singularity_wrapper = rec_parameters["singularity_wrapper"]

    if container_argument:  # isfile cannot handle None
        if os.path.isfile(container_argument):
            container_name = container_argument
        else:
            sys.exit("The path to container is not a file.")

    return container_name, singularity_wrapper


def main(arguments):
    container_name, singularity_wrapper = load_container_parameters(arguments.container)
    wav_path_for_container = "/opt/kaldi/egs/src_for_wav/"
    target_path_for_container = "/opt/kaldi/egs/temp/"

    input_directory, filename_with_extension = os.path.split(arguments.inputfile)
    filename, _ = os.path.splitext(filename_with_extension)
    abspath_inputdir = os.path.abspath(input_directory)
    abspath_targetdir = os.path.abspath(arguments.targetdir)

    bind_input = "-B {}:{}".format(abspath_inputdir, wav_path_for_container)
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
