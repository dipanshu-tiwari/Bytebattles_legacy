FROM alpine

RUN addgroup -S runner
RUN adduser -S -G runner run
RUN apk add --no-cache gcc
RUN apk add --no-cache musl-dev

WORKDIR /home/run
RUN mkdir -p sandbox
RUN mkdir -p sandbox/sub
RUN mkdir -p sandbox/testcases

CMD /bin/sh
