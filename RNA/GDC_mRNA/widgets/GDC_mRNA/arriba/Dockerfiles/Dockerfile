From ubuntu:18.04
Maintainer Ling-Hong Hung
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends supervisor \
    build-essential samtools r-base rna-star wget ca-certificates libcurl4-openssl-dev libxml2-dev \
    && Rscript -e 'install.packages("circlize", repos="http://cran.r-project.org"); source("https://bioconductor.org/biocLite.R"); biocLite(c("GenomicRanges", "GenomicAlignments"))'
    && apt-get remove build-essential ca-certificates libcurl4-openssl-dev libxml2-dev \
    && apt-get clean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - "https://github.com/suhrig/arriba/releases/download/v1.1.0/arriba_v1.1.0.tar.gz" | tar -xzf -
