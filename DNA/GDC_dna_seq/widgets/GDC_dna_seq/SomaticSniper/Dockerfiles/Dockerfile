FROM debian:buster-slim
COPY bam-somaticsniper /usr/local/bin/bam-somaticsniper
RUN mkdir -p /usr/local/share/doc/somatic-sniper1.0.5/
COPY copyright  /usr/local/share/doc/somatic-sniper1.0.5/copyright
COPY run_sniper.sh /usr/local/bin/run_sniper.sh
