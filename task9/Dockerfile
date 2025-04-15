FROM alpine

RUN apk update && apk add iputils tcpdump bash
COPY ping_test.sh /ping_test.sh
CMD ["/bin/bash"]
