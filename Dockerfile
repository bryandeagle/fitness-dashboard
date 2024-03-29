FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ntp libxml2-dev libxslt-dev python3-pip python3-dev
RUN ntpd -gq && service ntp start
COPY app /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3","-u"]
CMD ["app.py"]