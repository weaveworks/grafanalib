FROM alpine:3.6
RUN apk add --no-cache --upgrade python3
RUN python3 -m ensurepip && pip3 install --upgrade pip
COPY requirements.txt /
RUN pip3 install -r requirements.txt
COPY gfdatasource /
ENTRYPOINT ["/gfdatasource"]

ARG revision
LABEL works.weave.role="system" \
      maintainer="Weaveworks <help@weave.works>" \
      org.opencontainers.image.title="grafanalib" \
      org.opencontainers.image.source="https://github.com/weaveworks/grafanalib" \
      org.opencontainers.image.revision="${revision}" \
      org.opencontainers.image.vendor="Weaveworks"
