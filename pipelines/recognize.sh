#!/bin/bash

project_dir=/opt/kaldi/egs/kaldi-rec/s5

cd "$project_dir"

. ./path.sh

arguments="$*"

python finnish-forced-alignment/pipelines/kaldi-rec-py2 $arguments

# for loop all .ctm files. use basename etc. check previous scripts. if no files works. should not be two files. delete after loop just in case?
for ctm in *.ctm # should be only one, if there is any
do
  python3 finnish-forced-alignment/data_preparation/ctm2results.py $ctm
done

for txt in *.txt # should be only one, if there is any
do
  sed -i 's/NULL: //' $txt
done
