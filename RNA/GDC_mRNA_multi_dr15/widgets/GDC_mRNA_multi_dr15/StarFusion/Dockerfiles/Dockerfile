FROM debian:buster-slim
Maintainer Ling-Hong Hung
ENV DEBIAN_FRONTEND=noninteractive
ENV STAR_FUSION_VERSION 1.4.0
ENV SAMTOOLS_VERSION 1.9
ENV HTSLIB_VERSION 1.9

RUN apt-get update && apt-get install -y libgomp1 libbz2-dev wget build-essential libdb-dev libz-dev libcurl4-openssl-dev  liblzma-dev libncurses5-dev \
    && wget -qO- https://github.com/samtools/samtools/releases/download/${SAMTOOLS_VERSION}/samtools-${SAMTOOLS_VERSION}.tar.bz2 | tar -xjvf - \
    && cd /samtools-${SAMTOOLS_VERSION} && ./configure &&  make  \
    && mv /samtools-${SAMTOOLS_VERSION}/samtools /bin/ \
    && cd htslib-${HTSLIB_VERSION}/ && ./configure && make \
    && mv htsfile libhts.so* tabix bgzip /bin \
    && cd /root && rm -rf /samtools* \
    && wget -O - http://cpanmin.us | perl - --self-upgrade \
    && cpanm Data::Dumper FindBin DB_File URI::Escape Set::IntervalTree Carp::Assert JSON::XS PerlIO::gzip \
    && wget -qO- https://github.com/STAR-Fusion/STAR-Fusion/releases/download/STAR-Fusion-v${STAR_FUSION_VERSION}/STAR-Fusion-v${STAR_FUSION_VERSION}.FULL.tar.gz \
    | tar -xzvf - \
    && mv STAR-Fusion-v${STAR_FUSION_VERSION} STAR-Fusion \
    && apt-get remove -y wget build-essential \
    && apt-get clean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
RUN touch /usr/local/bin/STAR
RUN chmod +x /usr/local/bin/STAR
RUN sed -i 's/\&check_compatible_STAR/\#&check_compatible_STAR/' /root/STAR-Fusion/STAR-Fusion
