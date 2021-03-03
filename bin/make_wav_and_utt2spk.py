#!/usr/bin/env python3

import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Makes files kaldi needs for alignment.')
    parser.add_argument('tgtpath', type=str,
                        help='The path to the target directory.')
    parser.add_argument('wavpath', type=str,
                        help='The path to the wav files.')
    parser.add_argument('--txtpath', type=str,
                        help='The path to text files.')
    args = parser.parse_args()
    return args


def make_wav(wavpath, tgtpath):
    wav_name = os.path.join(tgtpath, "data/align/wav.scp")
    utt2spk_name = os.path.join(tgtpath, "data/align/utt2spk")
    spk2utt_name = os.path.join(tgtpath, "data/align/spk2utt")

    with open(wav_name, "w", encoding="utf-8") as wavlist_file,\
        open(utt2spk_name, "w", encoding="utf-8") as utt2spk_file,\
        open(spk2utt_name, "w", encoding="utf-8") as spk2utt_file:

        listofwavs = []
        if os.path.isdir(wavpath):
            listofwavs = sorted(os.listdir(wavpath))
        elif os.path.isfile(wavpath):
            listofwavs.append(os.path.split(wavpath)[1])
            wavpath = os.path.split(wavpath)[0]

        for wavfile in listofwavs:
            filename, file_extension = os.path.splitext(wavfile)
            if file_extension == ".wav":
                wavlist_file.write(filename + " " + os.path.join(wavpath, wavfile) + "\n")

                utt2spk_file.write(filename + " " + filename + "\n")
                spk2utt_file.write(filename + " " + filename + "\n")


def make_txt(txtpath, tgtpath):
    text_name = os.path.join(tgtpath, "data/align/text")
    with open(text_name, "w", encoding="utf-8") as text_file:
        listoftxts = []
        if os.path.isdir(txtpath):
            listoftxts = sorted(os.listdir(txtpath))
        elif os.path.isfile(txtpath):
            listoftxts.append(os.path.split(txtpath)[1])
            txtpath = os.path.split(txtpath)[0]

        for txtfile in listoftxts:
            filename, file_extension = os.path.splitext(txtfile)
            if file_extension == ".txt":
                utterances = []
                with open(os.path.join(txtpath, txtfile), 'r', encoding='utf-8') as utterance_file:
                    for line in utterance_file:
                        utterance = line.strip()
                        if len(utterance) == 0:
                            continue
                        utterances.append(utterance)

                text_file.write(filename + " " + " ".join(utterances) + "\n")


def main(arguments):
    make_wav(arguments.wavpath, arguments.tgtpath)
    if arguments.txtpath:
        make_txt(arguments.txtpath, arguments.tgtpath)
    else:
        make_txt(arguments.wavpath, arguments.tgtpath)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
