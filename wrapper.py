#!/usr/bin/env python
# coding: utf-8

# Imports
import argparse
import os
import sys
import subprocess


def parse_arguments():
    parser = argparse.ArgumentParser(description='Kaldi ASR')

    parser.add_argument('input', help='input, media filename (wav,mp4,avi,webm) or YouTube link',nargs=1)
    parser.add_argument('target', type=str, help='The target directory for files')
    parser.add_argument('--eaf',dest='eaf_filename',type=str,help='Outputs recognition result as EAF file',required=False)
    parser.add_argument('--srt',dest='srt_filename',type=str,help='Outputs recognition result as SRT subtitle file',required=False)
    parser.add_argument('--txt',dest='txt_filename',type=str,help='Outputs recognition results as normal text file',required=False)
    parser.add_argument('--diarization',dest='diarization',type=str,help='Diarization algorithm (LIUM)',choices=['LIUM'],required=False)
    parser.add_argument('-M', '--model', help='ASR model to use; "-M list" for list [default "%(default)s"]',default=default_args['model'],
                            metavar='M', choices=['list']+list(asr_models.keys()),action=ModelAction)
    args = parser.parse_args()

    return args


def main(arguments):
    rc = subprocess.call(
        ["/tmp/matthies/align.sh",
         csv_file,
         debug,
         arguments.targetdir,
         arguments.datadir])


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
