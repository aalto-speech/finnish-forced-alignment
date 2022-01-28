#!/bin/bash
# align will be copied from outside

csv_file=$1
debugBoolean=$2
textDirBoolean=$3
src_for_wav=$4
src_for_txt=$5

project_dir=/opt/kaldi/egs/kohdistus
src_for_mdl=/opt/kaldi/egs/align

cd "$project_dir"

bin_folder=/opt/kaldi/egs/align/aligning_with_Docker/bin

ln -s ../wsj/s5/utils utils
ln -s ../wsj/s5/steps steps
ln -s "$src_for_mdl"/conf conf

mkdir exp
mkdir -p data/align

ln -s "$src_for_mdl"/exp/nnet3 exp/nnet3

cp ../wsj/s5/path.sh .

sed -i '1 s/...$//' path.sh

mkdir data/dict
mkdir data/lang

cat <<EOF > data/dict/optional_silence.txt
SIL
EOF

cat <<EOF > data/dict/silence_phones.txt
SIL
SPN
NSN
EOF

cat <<EOF > data/dict/nonsilence_phones.txt
A
AE
B
D
E
F
G
H
I
J
K
L
M
N
O
OE
P
R
S
T
U
V
Y
EOF

if [ "$textDirBoolean" = "textDirTrue" ]
then
  python3 $bin_folder/make_wav_and_utt2spk.py "$project_dir" "$src_for_wav" --txtpath "$src_for_txt"
else
  python3 $bin_folder/make_wav_and_utt2spk.py "$project_dir" "$src_for_wav"
fi

sed -i 's/!sil/!SIL/g' data/align/text
sed -i 's/<unk>/<UNK>/g' data/align/text

cut -f 2- -d ' ' data/align/text > corpus

python3 $bin_folder/change_lex_pho.py corpus $bin_folder/$csv_file
mv lexicon.txt data/dict

extra=3
utils/prepare_lang.sh --num-extra-phone-disambig-syms $extra data/dict "<UNK>" data/lang/local data/lang

utils/fix_data_dir.sh data/align

utils/copy_data_dir.sh data/align data/align_hires

nj=1

steps/make_mfcc.sh --nj $nj --mfcc-config conf/mfcc_hires.conf --cmd "run.pl" data/align_hires
steps/compute_cmvn_stats.sh data/align_hires

utils/fix_data_dir.sh data/align_hires

steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj $nj data/align_hires exp/nnet3/extractor exp/align/ivectors_hires

steps/nnet3/align.sh --nj 1 --use_gpu false --online_ivector_dir exp/align/ivectors_hires data/align_hires/ data/lang/ exp/nnet3/chain/ exp/align_ali

steps/get_train_ctm.sh data/align_hires data/lang exp/align_ali
cp exp/align_ali/ct* .
python3 $bin_folder/ctm2results.py ctm

if [ "$debugBoolean" = "true" ]
then
  cp data/align/text .
  cp data/align/wav.scp .
  cp data/dict/lexicon.txt .
fi
rm corpus path.sh conf steps utils
rm -r exp data
