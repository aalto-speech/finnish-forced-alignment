#!/bin/bash

project_dir=/opt/kaldi/egs/kaldi-rec/s5

cd "$project_dir"

. ./path.sh

arguments="$*"

python kaldi-rec $arguments

