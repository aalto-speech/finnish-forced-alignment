#!/usr/bin/env python3

import os
import sys


wav_name = "data/align/wav.scp"
utt2spk_name = "data/align/utt2spk"
basepath = "data/src/wavs"

with open(wav_name, "w", encoding="utf-8") as wavlist_file,\
    open(utt2spk_name, "w", encoding="utf-8") as utt2spk_file:

    for dirfile in sorted(os.listdir(basepath)):
        filename, file_extension = os.path.splitext(dirfile)
        if file_extension == ".wav":
            wavlist_file.write(filename + " " + os.path.join(basepath, dirfile) + "\n")

            utt2spk_file.write(filename + " " + filename + "\n")
