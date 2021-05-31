# Finnish-Forced-Alignment

This repository contains:
#1 Code used in a forced aligner for Finnish that can also be used in cross-language forced alignment.
#2 Code used for Finnish speech recognizer that also creates an alignment for the recognized words and the audio.

## Structure
- **analysis** : Scripts to calculate an alignment score for the results.
- **data-preparation** : Scripts to prepare the data for alignment, scoring, and output files.
- **g2p-mappings** : The grapheme to phoneme mappings used in cross-language alignment.
- **interfaces** : Python files that apply argparse to create a commandline interface for the user.
- **pipelines** : Files that go through the necessary steps for producing the desired outputs from the given inputs.
- **tests** : Contains the tests to see that everything is still fine after making updates.
- **wrappers** : A wrapper for cluster computing environments to give parameters such as memory use, time or nodes.
- **Dockerfile** : A dockerfile that created the aligner.
- **LICENSE** : License-file.
- **README** : Readme-file.
- **kaldi-align_Dockerfile** : A dockerfile that created the aligner.
- **kaldi-asr_Dockerfile** : A dockerfile that created the speech recognizer container.

## Citation
For the forced aligner:
J. Leinonen, S. Virpioja and M. Kurimo. "Grapheme-Based Cross-Language Forced Alignment: Results with Uralic Languages" NoDaLiDa. 2021.

A BibTex will be provided later.

## Contact information
See the Github accounts, or emails from the paper given as citation.

The Docker container can be found in https://hub.docker.com/r/juholeinonen/kaldi-align
