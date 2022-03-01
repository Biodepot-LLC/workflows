FROM ubuntu:18.04
MAINTAINER varikmp<varikmp@uw.edu>
ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root
WORKDIR /root
RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates python3 curl python3-pip jq \
    && curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-370.0.0-linux-x86_64.tar.gz && tar -xvf google-cloud-sdk-370.0.0-linux-x86_64.tar.gz && rm google-cloud-sdk-370.0.0-linux-x86_64.tar.gz \
    && ln -sf /root/google-cloud-sdk/bin/gcloud /usr/bin/gcloud \
    && ln -sf /root/google-cloud-sdk/bin/gsutil /usr/bin/gsutil \
    && apt-get autoclean -y && apt-get autoremove -y --purge && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apk*
COPY dicomup.sh .
RUN chmod +x /root/dicomup.sh
ENTRYPOINT ["/root/dicomup.sh"]
