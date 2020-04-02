FROM alpine:3.11
RUN apk add curl bash
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh 
RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]
ENTRYPOINT ["docker-entrypoint.sh"]