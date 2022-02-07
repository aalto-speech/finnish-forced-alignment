#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from dataclasses import dataclass

import pandas as pd
import torch
import torchaudio
from torchaudio.models.wav2vec2.utils import import_huggingface_model
from transformers import Wav2Vec2ForCTC

torch.random.manual_seed(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

sample_rate = 16000
finnish_labels_dict = {"<pad>": 0,
                       "<s>": 1,
                       "</s>": 2,
                       "<unk>": 3,
                       "|": 4,
                       "E": 5,
                       "T": 6,
                       "A": 7,
                       "O": 8,
                       "N": 9,
                       "I": 10,
                       "H": 11,
                       "S": 12,
                       "R": 13,
                       "D": 14,
                       "L": 15,
                       "U": 16,
                       "M": 17,
                       "W": 18,
                       "C": 19,
                       "F": 20,
                       "G": 21,
                       "Y": 22,
                       "P": 23,
                       "B": 24,
                       "V": 25,
                       "K": 26,
                       "'": 27,
                       "X": 28,
                       "J": 29,
                       "Q": 30,
                       "Z": 31,
                       "Ä": 32,
                       "Ö": 33,
                       "Å": 34}


def parse_arguments():
    parser = argparse.ArgumentParser(description='Forced alignment with Wav2vec2 with CTC.')
    parser.add_argument('text', type=str,
                        help='Kaldi text file, contains utterance IDs and the utterance per line.')
    parser.add_argument('wav_list', type=str,
                        help='Kaldi wav.scp file, contains utterance IDs and path to the audio file.')
    parser.add_argument('checkpoint', type=str,
                        help='The path to the checkpoint directory of the pytorch wav2vec2 model.')
    parser.add_argument('ctm', type=str,
                        help='Results of alignment as a Kaldi ctm file.')
    args = parser.parse_args()
    return args


def get_trellis(emission, tokens, blank_id=0):
    num_frame = emission.size(0)
    num_tokens = len(tokens)

    # Trellis has extra diemsions for both time axis and tokens.
    # The extra dim for tokens represents <SoS> (start-of-sentence)
    # The extra dim for time axis is for simplification of the code.
    trellis = torch.full((num_frame + 1, num_tokens + 1), -float("inf"))
    trellis[:, 0] = 0
    for t in range(num_frame):
        trellis[t + 1, 1:] = torch.maximum(
            # Score for staying at the same token
            trellis[t, 1:] + emission[t, blank_id],
            # Score for changing to the next token
            trellis[t, :-1] + emission[t, tokens],
        )
    return trellis


@dataclass
class Point:
    token_index: int
    time_index: int
    score: float


# Merge the labels
@dataclass
class Segment:
    label: str
    start: int
    end: int
    score: float

    def __repr__(self):
        return f"{self.label}\t({self.score:4.2f}): [{self.start:5d}, {self.end:5d})"

    @property
    def length(self):
        return self.end - self.start


def backtrack(trellis, emission, tokens, blank_id=0):
    # Note:
    # j and t are indices for trellis, which has extra dimensions
    # for time and tokens at the beginning.
    # When referring to time frame index `T` in trellis,
    # the corresponding index in emission is `T-1`.
    # Similarly, when referring to token index `J` in trellis,
    # the corresponding index in transcript is `J-1`.
    j = trellis.size(1) - 1
    t_start = torch.argmax(trellis[:, j]).item()

    path = []
    for t in range(t_start, 0, -1):
        # 1. Figure out if the current position was stay or change
        # Note (again):
        # `emission[J-1]` is the emission at time frame `J` of trellis dimension.
        # Score for token staying the same from time frame J-1 to T.
        stayed = trellis[t - 1, j] + emission[t - 1, blank_id]
        # Score for token changing from C-1 at T-1 to J at T.
        changed = trellis[t - 1, j - 1] + emission[t - 1, tokens[j - 1]]

        # 2. Store the path with frame-wise probability.
        prob = emission[t - 1, tokens[j - 1] if changed > stayed else 0].exp().item()
        # Return token index and time index in non-trellis coordinate.
        path.append(Point(j - 1, t - 1, prob))

        # 3. Update the token
        if changed > stayed:
            j -= 1
            if j == 0:
                break
    else:
        raise ValueError("Failed to align")
    return path[::-1]


def merge_repeats(path, transcript):
    i1, i2 = 0, 0
    segments = []
    while i1 < len(path):
        while i2 < len(path) and path[i1].token_index == path[i2].token_index:
            i2 += 1
        score = sum(path[k].score for k in range(i1, i2)) / (i2 - i1)
        segments.append(
            Segment(
                transcript[path[i1].token_index],
                path[i1].time_index,
                path[i2 - 1].time_index + 1,
                score,
            )
        )
        i1 = i2
    return segments


# Merge words
def merge_words(segments, separator="|"):
    words = []
    i1, i2 = 0, 0
    while i1 < len(segments):
        if i2 >= len(segments) or segments[i2].label == separator:
            if i1 != i2:
                segs = segments[i1:i2]
                word = "".join([seg.label for seg in segs])
                score = sum(seg.score * seg.length for seg in segs) / sum(
                    seg.length for seg in segs
                )
                words.append(
                    Segment(word, segments[i1].start, segments[i2 - 1].end, score)
                )
            i1 = i2 + 1
            i2 = i1
        else:
            i2 += 1
    return words


def alignment2ctm(word_segments, utterance_ID, channel, ratio):
    ctm_list = []
    for word in word_segments:
        x0 = int(ratio * word.start)
        x1 = int(ratio * word.length)
        ctm_list.append(f"{utterance_ID} {channel} {x0 / sample_rate:.3f} {x1 / sample_rate:.3f} {word.label.lower()}")
    return ctm_list


def align_utterance(utterance, utterance_ID, wav_file, model):
    labels = tuple(finnish_labels_dict.keys())
    with torch.inference_mode():
        waveform, _ = torchaudio.load(wav_file)
        emissions, _ = model(waveform.to(device))
        emissions = torch.log_softmax(emissions, dim=-1)

    emission = emissions[0].cpu().detach()

    transcript_raw = utterance
    transcript = transcript_raw.upper().replace(" ", "|")
    dictionary = {c: i for i, c in enumerate(labels)}

    tokens = [dictionary[c] for c in transcript]

    trellis = get_trellis(emission, tokens)

    path = backtrack(trellis, emission, tokens)

    segments = merge_repeats(path, transcript)

    word_segments = merge_words(segments)

    ratio = waveform.size(1) / (trellis.size(0) - 1)

    return alignment2ctm(word_segments, utterance_ID, 1, ratio)


def main(text, wav_list, checkpoint, ctm):
    original = Wav2Vec2ForCTC.from_pretrained(checkpoint)
    model = import_huggingface_model(original).to(device)

    wav_dict = pd.read_csv(wav_list, names=["id", "path"], sep=" ").set_index('id')['path'].to_dict()

    with open(text, 'r', encoding='utf-8') as text_file, \
            open(ctm, 'w', encoding='utf-8') as ctm_file:
        for utterance_line in text_file:
            utterance_ID, utterance = utterance_line.rstrip().split(" ", maxsplit=1)
            if utterance_ID in wav_dict:
                utterance_ctm_lines = align_utterance(utterance, utterance_ID, wav_dict[utterance_ID], model)
                utterance_ctm_to_write = "\n".join(utterance_ctm_lines)
                ctm_file.write(utterance_ctm_to_write)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.text, arguments.wav_list, arguments.checkpoint, arguments.ctm)
