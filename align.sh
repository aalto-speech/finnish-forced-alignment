#!/bin/bash
#The whole point of this shell script is that it can be made into slurm easier than python

lang=$1
debug=$2
targetdir=$3
wavdir=$4

targetdir_path=$(readlink -f "$targetdir")
wavdir_path=$(readlink -f "$wavdir")

container=/tmp/matthies/kaldi-aligner-4.1.sif

if [ $# = 5 ]
then
  txtdir=$5
  txtdir_path=$(readlink -f "$txtdir")
  singularity run \
    -B "$wavdir_path":/opt/kaldi/egs/src_for_wav \
    -B "$txtdir_path":/opt/kaldi/egs/src_for_txt \
    -B "$targetdir_path":/opt/kaldi/egs/kohdistus \
    "$container" \
    "$lang" \
    "$debug" \
    "textDirTrue"
else
  singularity run \
    -B "$wavdir_path":/opt/kaldi/egs/src_for_wav \
    -B "$targetdir_path":/opt/kaldi/egs/kohdistus \
    "$container" \
    "$lang" \
    "$debug" \
    "textDirFalse"
fi
