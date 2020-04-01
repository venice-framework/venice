FROM alpine:3.11
#RUN apt-get update && apt-get install curl -y
RUN apk add curl bash
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh 
RUN ["chmod", "+x", "/usr/local/bin/docker-entrypoint.sh"]
ENTRYPOINT ["docker-entrypoint.sh"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]
