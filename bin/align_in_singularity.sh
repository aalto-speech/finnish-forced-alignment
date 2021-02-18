#!/bin/bash
# align will be copied from outside

if [ $# != 3 ]; then

  echo "You're doing this wrong"
  exit 1;
fi

csv_file=$1
datadir_ready=$2
project_dir=$3
src_for_align=../src_for_align

cd /opt/kaldi/egs/"$project_dir"


bin_folder=aligning_with_Docker/bin

ln -s ../wsj/s5/utils utils
ln -s ../wsj/s5/steps steps
ln -s data/src/conf conf

mkdir exp
ln -s data/src/exp/nnet3 exp/nnet3

cp ../wsj/s5/path.sh .

sed -i '1 s/...$//' path.sh

mkdir -p data/dict
mkdir data/lang

cat <<EOF > data/dict/optional_silence.txt
SIL
EOF

cat <<EOF > data/dict/silence_phones.txt
NSN
SIL
SPN
EOF

cat <<EOF > data/dict/nonsilence_phones.txt
2
A
I
N
U
b
d
e
f
g
h
j
k
l
m
n
o
p
r
s
t
v
y
{
EOF

if [ "$datadir_ready" = "false" ]
then
  python3 $bin_folder/make_wav_and_utt2spk.py "$src_for_align"/wavs
  utils/utt2spk_to_spk2utt.pl data/align/utt2spk > data/align/spk2utt
  cp "$src_for_align"/txts/text data/align/text
else
  cp "$src_for_align"/align/* data/align/
fi

sed -i 's/!sil/!SIL/g' data/align/text
sed -i 's/<unk>/<UNK>/g' data/align/text

cut -f 2- -d ' ' data/align/text > corpus

python3 $bin_folder/change_lex_pho.py corpus $bin_folder/$csv_file
mv lexicon.txt data/dict

extra=3
utils/prepare_lang.sh --num-extra-phone-disambig-syms $extra data/dict "<UNK>" data/lang/local data/lang

mkdir -p exp/align
cp exp/nnet3/chain/tree exp/align
cp exp/nnet3/chain/final.mdl exp/align

utils/fix_data_dir.sh data/align

utils/copy_data_dir.sh data/align data/align_hires

nj=1

steps/make_mfcc.sh --nj $nj --mfcc-config conf/mfcc_hires.conf --cmd "run.pl" data/align_hires
steps/compute_cmvn_stats.sh data/align_hires

utils/fix_data_dir.sh data/align_hires

steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj $nj data/align_hires exp/nnet3/extractor exp/nnet3/ivectors_align_hires

steps/nnet3/align.sh --nj 1 --use_gpu false --online_ivector_dir exp/nnet3/ivectors_align_hires data/align_hires/ data/lang/ exp/nnet3/chain/ exp/align_ali

steps/get_train_ctm.sh data/align_hires data/lang exp/align_ali
ctm_folder_name="$(date +"%Y_%m_%d_%I_%M_%p")_ctm"
mkdir data/src/txts/"$ctm_folder_name"
cp exp/align_ali/ct* data/src/txts/"$ctm_folder_name"

