#!/bin/bash
#The whole point of this shell script is that it can be made into slurm easier than python

lang=$1
debug=$2
singlefile=$3
targetdir=$4
wavdir=$5

wav_path_for_container=""
txt_path_for_container=""

target_path_for_binding=$(readlink -f "$targetdir")
wav_path_for_binding=$(readlink -f "$wavdir")

container=/tmp/matthies/kaldi-aligner-5.0.sif

if [ "$singlefile" = "alignWholeDirectory" ]
then
  wav_path_for_container=/opt/kaldi/egs/src_for_wav
  txt_path_for_container=/opt/kaldi/egs/src_for_txt
else
  wav_path_for_container=/opt/kaldi/egs/src_for_wav/"$singlefile".wav
  txt_path_for_container=/opt/kaldi/egs/src_for_txt/"$singlefile".txt
fi

if [ $# = 6 ]
then
  txtdir=$6
  txt_path_for_binding=$(readlink -f "$txtdir")
  singularity run \
    -B "$wav_path_for_binding":/opt/kaldi/egs/src_for_wav \
    -B "$txt_path_for_binding":/opt/kaldi/egs/src_for_txt \
    -B "$target_path_for_binding":/opt/kaldi/egs/kohdistus \
    "$container" \
    "$lang" \
    "$debug" \
    "textDirTrue" \
    "$wav_path_for_container" \
    "$txt_path_for_container"
else
  singularity run \
    -B "$wavdir_path":/opt/kaldi/egs/src_for_wav \
    -B "$target_path_for_binding":/opt/kaldi/egs/kohdistus \
    "$container" \
    "$lang" \
    "$debug" \
    "textDirFalse" \
    "$wav_path_for_container" \
    "$txt_path_for_container"
fi
