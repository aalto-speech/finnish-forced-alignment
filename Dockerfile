FROM kaldiasr/kaldi@sha256:4b5153e87f8ec61ef96bcf1751ba97e9e39b05aedf24bea37886a54944fb44ef

WORKDIR /opt/kaldi/egs/align

# Creating Kaldi file structure
RUN mkdir -p data/align
RUN mkdir -p data/src
RUN mkdir -p exp/nnet3/chain
RUN mkdir -p exp/nnet3/extractor
RUN mkdir -p conf

# Loading the helper scripts
RUN git clone https://github.com/juholeinonen/aligning_with_Docker.git
WORKDIR aligning_with_Docker
RUN git reset --hard 8f80ab9 
WORKDIR /opt/kaldi/egs/align

# Copying file by file for sake of transparency the DNN
COPY exp/nnet3/chain/cmvn_opts exp/nnet3/chain/cmvn_opts
COPY exp/nnet3/chain/final.mdl exp/nnet3/chain/final.mdl
COPY exp/nnet3/chain/tree exp/nnet3/chain/tree

# Copying file by file for sake of transparency the i-vector extractor
COPY exp/nnet3/extractor/final.dubm exp/nnet3/extractor/final.dubm
COPY exp/nnet3/extractor/final.ie exp/nnet3/extractor/final.ie
COPY exp/nnet3/extractor/final.ie.id exp/nnet3/extractor/final.ie.id
COPY exp/nnet3/extractor/final.mat exp/nnet3/extractor/final.mat
COPY exp/nnet3/extractor/global_cmvn.stats exp/nnet3/extractor/global_cmvn.stats
COPY exp/nnet3/extractor/online_cmvn.conf exp/nnet3/extractor/online_cmvn.conf
COPY exp/nnet3/extractor/splice_opts exp/nnet3/extractor/splice_opts

COPY conf/mfcc_hires.conf conf/mfcc_hires.conf

ENTRYPOINT ["./aligning_with_Docker/bin/align_from_scratch.sh"]
