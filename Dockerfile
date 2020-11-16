FROM kaldiasr/kaldi@sha256:4b5153e87f8ec61ef96bcf1751ba97e9e39b05aedf24bea37886a54944fb44ef

WORKDIR /opt/kaldi/egs/align
ADD bin .
RUN mkdir -p data/align
RUN mkdir -p data/src
RUN mkdir -p exp
RUN mkdir -p conf
COPY exp exp
COPY conf conf
ENTRYPOINT ["./align_from_scratch.sh"]
