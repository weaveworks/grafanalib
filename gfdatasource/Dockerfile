FROM alpine:3.6
LABEL works.weave.role=system
RUN apk add --no-cache --upgrade python3
RUN python3 -m ensurepip && pip3 install --upgrade pip
COPY requirements.txt /
RUN pip3 install -r requirements.txt
COPY gfdatasource /
ENTRYPOINT ["/gfdatasource"]
