#!/bin/bash

lang=$1
targetdir=$2
wavdir=$3

targetdir_path=$(readlink -f "$targetdir")
wavdir_path=$(readlink -f "$wavdir")

container=/tmp/matthies/kaldi-aligner-4.0.sif

if [ $# = 4 ]
then
  txtdir=$4
  txtdir_path=$(readlink -f "$txtdir")
  singularity run -B "$wavdir_path":/opt/kaldi/egs/src_for_wav -B "$txtdir_path":/opt/kaldi/egs/src_for_txt -B "$targetdir_path":/opt/kaldi/egs/kohdistus "$container" "$lang" "yes"
else
  singularity run -B "$wavdir_path":/opt/kaldi/egs/src_for_wav -B "$targetdir_path":/opt/kaldi/egs/kohdistus "$container" "$lang" "no"
fi
