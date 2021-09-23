#!/bin/bash

project_dir=/opt/kaldi/egs/kaldi-rec/s5

cd "$project_dir"

. ./path.sh

arguments="$*"

python finnish-forced-alignment/pipelines/kaldi-rec-py2 $arguments

for txt in ../../temp/*.txt # should be only one, if there is any
do
  if [ -f $txt ]; then
  sed -i 's/NULL: //' $txt
  fi
done
