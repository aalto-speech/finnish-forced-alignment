#!/bin/bash
#The whole point of this shell script is that it can be made into slurm easier than python

arguments="$*"

singularity run $arguments 
