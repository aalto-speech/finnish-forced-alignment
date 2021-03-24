#!/bin/bash
#The whole point of this shell script is that it can be made into slurm easier than python

wrapper=$1
targetdir=$2
cscdir=$3

echo "Testing wrong samplerate, here 22100Hz, should be 16000Hz"
python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug

read -p "Press enter to continue"


echo "Testing changing samplerate and sami alignment"
python3 "$wrapper" "$targetdir" --datadir "$cscdir"/giellagas_data_dir --lang se --debug

read -p "Press enter to continue"


echo "Testing giving txt and wav directories and estonian alignment"
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --wav "$cscdir"/estonian_wav_dir --lang et --debug

read -p "Press enter to continue"


echo "Testing wrong inputs (no txt when wav and no wav when txt)"
python3 "$wrapper" "$targetdir" --wav "$cscdir"/estonian_wav_dir --lang et --debug
python3 "$wrapper" "$targetdir" --txt "$cscdir"/estonian_txt_dir --lang et --debug

read -p "Press enter to continue"
