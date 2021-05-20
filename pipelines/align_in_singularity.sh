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

mkdir -p exp/align
ln -s exp/nnet3/chain/tree exp/align/tree
ln -s exp/nnet3/chain/final.mdl exp/align/final.mdl

utils/fix_data_dir.sh data/align

utils/copy_data_dir.sh data/align data/align_hires

nj=1

steps/make_mfcc.sh --nj $nj --mfcc-config conf/mfcc_hires.conf --cmd "run.pl" data/align_hires
steps/compute_cmvn_stats.sh data/align_hires

utils/fix_data_dir.sh data/align_hires

steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj $nj data/align_hires exp/nnet3/extractor exp/align/ivectors_hires

steps/nnet3/align.sh --nj 1 --use_gpu false --online_ivector_dir exp/align/ivectors_hires data/align_hires/ data/lang/ exp/nnet3/chain/ exp/align_ali

steps/get_train_ctm.sh data/align_hires data/lang exp/align_ali
ctm_folder_name="$(date +"%Y_%m_%d_%H_%M_%S")"
mkdir "$ctm_folder_name"
cp exp/align_ali/ct* "$ctm_folder_name"
python3 $bin_folder/ctm2results.py "$ctm_folder_name"/ctm

if [ "$debugBoolean" = "true" ]
then
  cp data/align/text $ctm_folder_name
  cp data/align/wav.scp $ctm_folder_name
  cp data/dict/lexicon.txt $ctm_folder_name
fi
rm corpus path.sh conf steps utils
rm -r exp data
