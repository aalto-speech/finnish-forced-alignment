#!/bin/bash
#The whole point of this shell script is that it can be made into slurm easier than python

wrapper=$1
targetdir=$2
cscdir=$3

echo "Testing aligning only one file. Both files in same directory but given separate."
echo "python3 "$wrapper" "$targetdir" --wav "$cscdir"/yle_data_dir/koko_1.wav --txt "$cscdir"/yle_data_dir/koko_1.txt --lang fi --debug"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --wav "$cscdir"/yle_wav_dir/koko_1.wav --txt "$cscdir"/yle_txt_dir/koko_1.txt --lang fi --debug

echo "Testing wrong samplerate, here 22100Hz, should be 16000Hz"
echo "python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug


echo "Testing changing samplerate and sami alignment"
echo "python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug


echo "Testing giving txt and wav directories and estonian alignment"
echo "python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --wav "$cscdir"/estonian_wav_dir --lang et --debug"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --wav "$cscdir"/estonian_wav_dir --lang et --debug


echo "Testing wrong inputs (no txt when wav and no wav when txt)"
echo "python3 "$wrapper" "$targetdir" --wav "$cscdir"/estonian_wav_dir --lang et --debug"
echo "python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --lang et --debug"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --wav "$cscdir"/estonian_wav_dir --lang et --debug
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --lang et --debug


echo "Testing wrong amount of files (txt then wav)"
echo "python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --wav "$cscdir"/estonian_not_all_wavs --lang et --debug"
echo "python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_not_all_txts --wav "$cscdir"/estonian_wav_dir --lang et --debug"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --wav "$cscdir"/estonian_not_all_wavs --lang et --debug
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_not_all_txts --wav "$cscdir"/estonian_wav_dir --lang et --debug

echo "Testing english alignment"
echo "python3 "$wrapper" "$targetdir" --txt "$cscdir"/librispeech_txt_dir --wav "$cscdir"/librispeech_wav_dir --lang en --debug"
read -p "Press enter to continue"
python3 "$wrapper" "$targetdir" --txt "$cscdir"/librispeech_txt_dir --wav "$cscdir"/librispeech_wav_dir --lang en --debug
