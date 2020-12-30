FROM debian:buster-slim
MAINTAINER Hong Hung
ENV PATH=$PATH:/usr/local/bin
RUN apt-get -y update && apt-get install -y wget
RUN wget -O /usr/local/bin/muse http://bioinformatics.mdanderson.org/Software/MuSE/MuSEv1.0rc_submission_c039ffa
RUN chmod +x /usr/local/bin/muse
COPY run_muse_call.sh /usr/local/bin/run_muse_call.sh

