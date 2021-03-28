#!/bin/bash
#The whole point of this shell script is that it can be made into slurm easier than python

wrapper=$1
targetdir=$2
cscdir=$3

echo "Testing wrong samplerate, here 22100Hz, should be 16000Hz"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug


echo "Testing changing samplerate and sami alignment"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug


echo "Testing giving txt and wav directories and estonian alignment"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --wav "$cscdir"/estonian_wav_dir --lang et --debug


echo "Testing wrong inputs (no txt when wav and no wav when txt)"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --wav "$cscdir"/estonian_wav_dir --lang et --debug
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --lang et --debug


echo "Testing wrong amount of files (txt then wav)"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --wav "$cscdir"/estonian_not_all_wavs --lang et --debug
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_not_all_txts --wav "$cscdir"/estonian_wav_dir --lang et --debug

echo "Testing english alignment"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --txt "$cscdir"/librispeech_txt_dir --wav "$cscdir"/librispeech_wav_dir --lang en --debug
