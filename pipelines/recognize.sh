#!/bin/bash

project_dir=/opt/kaldi/egs/kaldi-rec/s5

cd "$project_dir"

. ./path.sh

arguments="$*"

python finnish-forced-alignment/pipelines/kaldi-rec-py2 $arguments

txt=($(python finnish-forced-alignment/pipelines/rec_util.py $arguments))

if [ -f $txt ]; then
  sed -i 's/S1: //' $txt
fi
