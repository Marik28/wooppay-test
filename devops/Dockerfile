FROM python:3.9.9-slim-buster

COPY requirements.txt requirements.txt
RUN set -ex \
	&& pip3 install -U pip setuptools \
    && pip3 install -r requirements.txt --no-cache-dir \
    && rm requirements.txt

COPY src src
WORKDIR src