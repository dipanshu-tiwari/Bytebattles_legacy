FROM alpine:latest

RUN addgroup -S runner \
 && adduser -S -G runner run

RUN apk add --no-cache python3

WORKDIR /home/run

RUN mkdir -p sandbox/sub sandbox/testcases \
 && chown -R run:runner /home/run

USER run

CMD ["python3"]
